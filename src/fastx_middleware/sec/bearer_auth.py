"""Bearer Token Authentication Middleware for FastMVC.

Token-based authentication using Bearer tokens.
"""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from fastx_middleware.mw_core.base import FastMVCMiddleware
from fastx_middleware.constants import *


@dataclass
class BearerAuthConfig:
    """Configuration for bearer auth middleware.

    Attributes:
        tokens: Dict of token -> user info.
        validate_func: Custom validation function.
        header_name: Authorization header name.
        realm: Authentication realm.

    """

    tokens: dict[str, dict[str, Any]] = field(default_factory=dict)
    header_name: str = HEADER_AUTHORIZATION
    realm: str = "API"
    return_error_detail: bool = False


class BearerAuthMiddleware(FastMVCMiddleware):
    """Middleware for Bearer Token Authentication.

    Validates Bearer tokens from Authorization header
    and attaches user info to request.

    Example:
        ```python
        from fastmiddleware import BearerAuthMiddleware

        app.add_middleware(
            BearerAuthMiddleware,
            tokens={
                "token123": {"user_id": 1, "role": "admin"},
                "token456": {"user_id": 2, "role": STATE_USER},
            },
        )
        ```

    """

    def __init__(
        self,
        app,
        config: BearerAuthConfig | None = None,
        tokens: dict[str, dict[str, Any]] | None = None,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            tokens: The tokens parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or BearerAuthConfig()

        if tokens:
            self.config.tokens = tokens

        self._validate_func = None

    def set_validate_func(self, func: Callable[[str], dict[str, Any] | None]) -> None:
        """Set custom token validation function."""
        self._validate_func = func

    def _extract_token(self, request: Request) -> str | None:
        """Extract bearer token from request."""
        auth = request.headers.get(self.config.header_name)

        if not auth:
            return None

        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        return parts[1]

    def _validate_token(self, token: str) -> dict[str, Any] | None:
        """Validate token and return user info."""
        if self._validate_func:
            return self._validate_func(token)

        return self.config.tokens.get(token)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Execute dispatch operation.

        Args:
            request: The request parameter.
            call_next: The call_next parameter.

        Returns:
            The result of the operation.
        """
        if self.should_skip(request):
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)

        token = self._extract_token(request)

        if not token:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={FIELD_ERROR: True, FIELD_MESSAGE: "Missing authentication token"},
                headers={HEADER_WWW_AUTHENTICATE: f'Bearer realm="{self.config.realm}"'},
            )

        user_info = self._validate_token(token)

        if not user_info:
            content = {FIELD_ERROR: True, FIELD_MESSAGE: "Invalid token"}
            if self.config.return_error_detail:
                content[FIELD_DETAIL] = "Token not found or expired"

            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content=content,
                headers={HEADER_WWW_AUTHENTICATE: f'Bearer realm="{self.config.realm}"'},
            )

        request.state.user = user_info
        request.state.token = token

        return await call_next(request)
