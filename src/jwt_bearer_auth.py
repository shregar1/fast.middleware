"""
JWT Bearer authentication middleware (injectable decode + user lookup).

Application code supplies callables for token decoding, session validation,
and JSON error responses so this package stays free of app models and DTOs.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from http import HTTPStatus
from typing import Any, Literal

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

from utils.request_id_context import get_request_id

ErrorKind = Literal[
    "missing_bearer",
    "session_expired",
    "auth_failed",
    "service_unavailable",
    "generic",
]


def default_resolve_request_urn(request: Request) -> str:
    """Prefer ``request.state.urn``, then ``request.state.request_id``, then context id."""
    urn = getattr(request.state, "urn", None)
    if urn:
        return str(urn)
    rid = getattr(request.state, "request_id", None)
    if rid:
        return str(rid)
    ctx = get_request_id()
    if ctx:
        return ctx
    return "unknown"


class JWTBearerAuthMiddleware(BaseHTTPMiddleware):
    """
    Validate ``Authorization: Bearer`` on protected routes; attach user to ``request.state``.

    Skips OPTIONS and paths in *unprotected_paths* or *callback_paths*.
    """

    def __init__(
        self,
        app,
        *,
        unprotected_paths: Iterable[str],
        callback_paths: Iterable[str],
        decode_bearer: Callable[[str, str], dict],
        load_user: Callable[[dict, str], Any | None],
        on_authenticated: Callable[[Request, dict], None],
        build_error_response: Callable[[str, ErrorKind, BaseException | None], JSONResponse],
        resolve_request_urn: Callable[[Request], str] | None = None,
        log: Any | None = None,
    ) -> None:
        super().__init__(app)
        self._unprotected = frozenset(unprotected_paths)
        self._callback = frozenset(callback_paths)
        self._decode = decode_bearer
        self._load_user = load_user
        self._on_auth = on_authenticated
        self._build_error = build_error_response
        self._urn = resolve_request_urn or default_resolve_request_urn
        self._log = log

    def _debug(self, msg: str, **kwargs: Any) -> None:
        if self._log is not None:
            self._log.debug(msg, **kwargs)

    async def dispatch(self, request: Request, call_next):
        urn = self._urn(request)
        endpoint = request.url.path

        if request.method == "OPTIONS":
            return await call_next(request)

        self._debug("Inside JWT bearer auth middleware", urn=urn)
        self._debug(f"Received request for endpoint: {endpoint}", urn=urn)

        if endpoint in self._unprotected or endpoint in self._callback:
            self._debug("Accessing unprotected/callback route", urn=urn)
            return await call_next(request)

        self._debug("Accessing protected route", urn=urn)
        raw = request.headers.get("authorization")
        if not raw or "bearer" not in raw.lower():
            self._debug("Preparing response metadata (missing bearer)", urn=urn)
            return self._build_error(urn, "missing_bearer", None)

        try:
            self._debug("Decoding bearer token", urn=urn)
            token = raw.split(" ", 1)[1].strip()
            user_data: dict = self._decode(token, urn)
            self._debug("Decoded bearer token", urn=urn)

            self._debug("Loading user session", urn=urn)
            user = self._load_user(user_data, urn)
            self._debug("Loaded user session", urn=urn)

            if not user:
                self._debug("Preparing response metadata (session expired)", urn=urn)
                return self._build_error(urn, "session_expired", None)

            self._on_auth(request, user_data)

        except (ValueError, KeyError) as err:
            self._debug(
                f"{err.__class__.__name__} while parsing auth header or token: {err}",
                urn=getattr(request.state, "urn", urn),
            )
            return self._build_error(urn, "auth_failed", err)

        except SQLAlchemyError as err:
            if self._log is not None:
                self._log.error(
                    f"{err.__class__.__name__} while querying user: {err}",
                    urn=getattr(request.state, "urn", urn),
                )
            return self._build_error(urn, "service_unavailable", err)

        except Exception as err:
            self._debug(
                f"{err.__class__.__name__} while authenticating JWT: {err}",
                urn=urn,
            )
            return self._build_error(urn, "generic", err)

        self._debug("Proceeding with request execution", urn=urn)
        response: Response = await call_next(request)
        return response
