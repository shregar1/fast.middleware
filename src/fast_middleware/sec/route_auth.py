"""Route-Based Authentication Middleware for FastMVC.

Applies different auth requirements per route.
"""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from fast_middleware.mw_core.base import FastMVCMiddleware
from fast_middleware.constants import *


@dataclass
class RouteAuth:
    """Route authentication requirement."""

    path: str
    methods: set[str] = field(default_factory=lambda: {"*"})
    require_auth: bool = True
    required_roles: list[str] = field(default_factory=list)
    required_scopes: list[str] = field(default_factory=list)


@dataclass
class RouteAuthConfig:
    """Configuration for route auth middleware.

    Attributes:
        routes: List of route auth requirements.
        default_require_auth: Default auth requirement.
        user_state_key: Key in request.state for user.

    """

    routes: list[RouteAuth] = field(default_factory=list)
    default_require_auth: bool = False
    user_state_key: str = STATE_USER


class RouteAuthMiddleware(FastMVCMiddleware):
    """Middleware that applies auth per route.

    Allows different authentication and authorization
    requirements for different routes.

    Example:
        ```python
        from fastmiddleware import RouteAuthMiddleware, RouteAuth

        app.add_middleware(
            RouteAuthMiddleware,
            routes=[
                RouteAuth("/api/public", require_auth=False),
                RouteAuth("/api/user", require_auth=True),
                RouteAuth("/api/admin", require_auth=True, required_roles=["admin"]),
            ],
        )
        ```

    """

    def __init__(
        self,
        app,
        config: RouteAuthConfig | None = None,
        routes: list[RouteAuth] | None = None,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            routes: The routes parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or RouteAuthConfig()

        if routes:
            self.config.routes = routes

    def _find_route(self, path: str, method: str) -> RouteAuth | None:
        """Find matching route auth config."""
        for route in self.config.routes:
            if not path.startswith(route.path):
                continue
            if "*" in route.methods or method in route.methods:
                return route
        return None

    def _get_user(self, request: Request) -> dict[str, Any] | None:
        """Get user from request state."""
        return getattr(request.state, self.config.user_state_key, None)

    def _check_roles(self, user: dict[str, Any], required: list[str]) -> bool:
        """Check if user has required roles."""
        user_roles = user.get("roles", [])
        return any(role in user_roles for role in required)

    def _check_scopes(self, user: dict[str, Any], required: list[str]) -> bool:
        """Check if user has required scopes."""
        user_scopes = user.get("scopes", [])
        return any(scope in user_scopes for scope in required)

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

        route_auth = self._find_route(request.url.path, request.method)

        if not route_auth:
            if not self.config.default_require_auth:
                return await call_next(request)
            route_auth = RouteAuth(
                path="",
                require_auth=True,
            )

        if not route_auth.require_auth:
            return await call_next(request)

        user = self._get_user(request)

        if not user:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={FIELD_ERROR: True, FIELD_MESSAGE: MSG_AUTHENTICATION_REQUIRED},
            )

        if route_auth.required_roles:
            if not self._check_roles(user, route_auth.required_roles):
                return JSONResponse(
                    status_code=HTTP_403_FORBIDDEN,
                    content={FIELD_ERROR: True, FIELD_MESSAGE: "Insufficient role"},
                )

        if route_auth.required_scopes:
            if not self._check_scopes(user, route_auth.required_scopes):
                return JSONResponse(
                    status_code=HTTP_403_FORBIDDEN,
                    content={FIELD_ERROR: True, FIELD_MESSAGE: "Insufficient scope"},
                )

        return await call_next(request)
