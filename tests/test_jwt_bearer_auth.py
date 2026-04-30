"""JWT bearer auth middleware (injectable hooks)."""

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fastx_middleware.sec.jwt_bearer_auth import JWTBearerAuthMiddleware


async def _ok(_request: Request):
    """Execute _ok operation.

    Args:
        _request: The _request parameter.

    Returns:
        The result of the operation.
    """
    return PlainTextResponse("ok")


def _json_err(urn: str, kind, _exc):
    """Execute _json_err operation.

    Args:
        urn: The urn parameter.
        kind: The kind parameter.
        _exc: The _exc parameter.

    Returns:
        The result of the operation.
    """
    return JSONResponse({"urn": urn, "kind": kind}, status_code=401)


def test_skips_options():
    """Execute test_skips_options operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/p", _ok, methods=["GET", "OPTIONS"])])
    app.add_middleware(
        JWTBearerAuthMiddleware,
        unprotected_paths=(),
        callback_paths=(),
        decode_bearer=lambda _t, _u: {},
        load_user=lambda _c, _u: object(),
        on_authenticated=lambda _r, _d: None,
        build_error_response=_json_err,
    )
    client = TestClient(app)
    r = client.options("/p")
    assert r.status_code == 200


def test_unprotected_path():
    """Execute test_unprotected_path operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/health", _ok)])
    app.add_middleware(
        JWTBearerAuthMiddleware,
        unprotected_paths=["/health"],
        callback_paths=(),
        decode_bearer=lambda _t, _u: {},
        load_user=lambda _c, _u: object(),
        on_authenticated=lambda _r, _d: None,
        build_error_response=_json_err,
    )
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200


def test_missing_bearer():
    """Execute test_missing_bearer operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/api/x", _ok)])
    app.add_middleware(
        JWTBearerAuthMiddleware,
        unprotected_paths=(),
        callback_paths=(),
        decode_bearer=lambda _t, _u: {},
        load_user=lambda _c, _u: object(),
        on_authenticated=lambda _r, _d: None,
        build_error_response=_json_err,
    )
    client = TestClient(app)
    r = client.get("/api/x")
    assert r.status_code == 401
    assert r.json()["kind"] == "missing_bearer"


def test_success_calls_on_authenticated():
    """Execute test_success_calls_on_authenticated operation.

    Returns:
        The result of the operation.
    """
    calls = []

    def on_auth(request, data):
        """Execute on_auth operation.

        Args:
            request: The request parameter.
            data: The data parameter.

        Returns:
            The result of the operation.
        """
        calls.append((request, data))
        request.state.user_id = data["user_id"]

    app = Starlette(routes=[Route("/api/x", _ok)])
    app.add_middleware(
        JWTBearerAuthMiddleware,
        unprotected_paths=(),
        callback_paths=(),
        decode_bearer=lambda _t, _u: {"user_id": 1, "user_urn": "u"},
        load_user=lambda _c, _u: object(),
        on_authenticated=on_auth,
        build_error_response=_json_err,
    )
    client = TestClient(app)
    r = client.get("/api/x", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert calls and calls[0][1]["user_id"] == 1
