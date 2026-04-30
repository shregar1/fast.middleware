"""No-Cache Middleware for FastMVC.

Disables caching for responses.
"""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

from starlette.requests import Request
from starlette.responses import Response

from fastx_middleware.mw_core.base import FastMVCMiddleware
from fastx_middleware.constants import *


@dataclass
class NoCacheConfig:
    """Configuration for no-cache middleware.

    Attributes:
        paths: Paths to apply no-cache (empty = all).
        methods: Methods to apply no-cache.
        headers: Cache control headers to add.

    """

    paths: set[str] = field(default_factory=set)
    methods: set[str] = field(default_factory=lambda: {"GET", "HEAD"})
    pragma: bool = True
    expires: bool = True


class NoCacheMiddleware(FastMVCMiddleware):
    """Middleware that disables caching.

    Adds headers to prevent caching of responses,
    useful for dynamic content or sensitive data.

    Example:
        ```python
        from fastmiddleware import NoCacheMiddleware

        app.add_middleware(
            NoCacheMiddleware,
            paths={"/api/user", "/api/session"},
        )

        # Responses will have:
        # Cache-Control: no-store, no-cache, must-revalidate
        # Pragma: no-cache
        # Expires: 0
        ```

    """

    def __init__(
        self,
        app,
        config: NoCacheConfig | None = None,
        paths: set[str] | None = None,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            paths: The paths parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or NoCacheConfig()

        if paths:
            self.config.paths = paths

    def _should_apply(self, path: str, method: str) -> bool:
        """Check if no-cache should apply."""
        if method not in self.config.methods:
            return False

        if not self.config.paths:
            return True

        return any(path.startswith(p) for p in self.config.paths)

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

        response = await call_next(request)

        if self._should_apply(request.url.path, request.method):
            response.headers[HEADER_CACHE_CONTROL] = (
                "no-store, no-cache, must-revalidate, private"
            )

            if self.config.pragma:
                response.headers[HEADER_PRAGMA] = "no-cache"

            if self.config.expires:
                response.headers[HEADER_EXPIRES] = "0"

        return response
