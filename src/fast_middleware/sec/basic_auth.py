"""Basic Authentication Middleware for FastMVC.

Simple HTTP Basic Authentication.
"""

import base64
import secrets
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

from starlette.requests import Request
from starlette.responses import Response

from fast_middleware.mw_core.base import FastMVCMiddleware
from fast_middleware.constants import *


@dataclass
class BasicAuthConfig:
    """Configuration for basic auth middleware.

    Attributes:
        users: Dict of username -> password.
        realm: Authentication realm.
        exclude_methods: Methods that don't require auth.

    """

    users: dict[str, str] = field(default_factory=dict)
    realm: str = "Restricted"
    exclude_methods: set[str] = field(default_factory=lambda: {"OPTIONS"})


class BasicAuthMiddleware(FastMVCMiddleware):
    """Middleware for HTTP Basic Authentication.

    Simple username/password authentication using
    the Authorization header.

    Example:
        ```python
        from fastmiddleware import BasicAuthMiddleware

        app.add_middleware(
            BasicAuthMiddleware,
            users={"admin": "secret123", STATE_USER: "password"},
        )
        ```

    """

    def __init__(
        self,
        app,
        config: BasicAuthConfig | None = None,
        users: dict[str, str] | None = None,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            users: The users parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or BasicAuthConfig()

        if users:
            self.config.users = users

    def _parse_auth(self, auth_header: str) -> tuple[str, str] | None:
        """Parse Authorization header."""
        if not auth_header.startswith("Basic "):
            return None

        try:
            encoded = auth_header[6:]
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
            return username, password
        except Exception:
            return None

    def _verify(self, username: str, password: str) -> bool:
        """Verify credentials."""
        if username not in self.config.users:
            return False

        stored = self.config.users[username]
        return secrets.compare_digest(password, stored)

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

        if request.method in self.config.exclude_methods:
            return await call_next(request)

        auth_header = request.headers.get(HEADER_AUTHORIZATION)

        if not auth_header:
            return Response(
                status_code=HTTP_401_UNAUTHORIZED,
                headers={HEADER_WWW_AUTHENTICATE: f'Basic realm="{self.config.realm}"'},
            )

        credentials = self._parse_auth(auth_header)

        if not credentials:
            return Response(
                status_code=HTTP_401_UNAUTHORIZED,
                headers={HEADER_WWW_AUTHENTICATE: f'Basic realm="{self.config.realm}"'},
            )

        username, password = credentials

        if not self._verify(username, password):
            return Response(
                status_code=HTTP_401_UNAUTHORIZED,
                headers={HEADER_WWW_AUTHENTICATE: f'Basic realm="{self.config.realm}"'},
            )

        request.state.user = username
        return await call_next(request)
