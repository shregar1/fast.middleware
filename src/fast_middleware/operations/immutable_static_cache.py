"""Long-lived immutable caching for versioned static assets (``/static/``, ``/assets/``, etc.)."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

from starlette.requests import Request
from starlette.responses import Response

from fast_middleware.mw_core.base import FastMVCMiddleware
from fast_middleware.constants import *


@dataclass
class ImmutableStaticCacheConfig:
    """Apply ``Cache-Control`` with ``immutable`` for matching URL paths.

    Paths match if the request path equals a prefix or starts with ``prefix + "/"``.
    Default prefixes suit hashed filenames under ``/static/`` and ``/assets/``.
    """

    path_prefixes: tuple[str, ...] = ("/static/", "/assets/")
    max_age_seconds: int = 31_536_000  # 1 year
    public: bool = True
    extra_directives: tuple[str, ...] = field(default_factory=tuple)


class ImmutableStaticCacheMiddleware(FastMVCMiddleware):
    """Set aggressive caching for static asset routes (fingerprints in filename).

    Example::

        from fastmiddleware import ImmutableStaticCacheMiddleware, ImmutableStaticCacheConfig

        app.add_middleware(
            ImmutableStaticCacheMiddleware,
            config=ImmutableStaticCacheConfig(
                path_prefixes=("/dist/", "/cdn/"),
                max_age_seconds=86_400,
            ),
        )
    """

    def __init__(
        self,
        app,
        config: ImmutableStaticCacheConfig | None = None,
        *,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or ImmutableStaticCacheConfig()

    def _matches(self, path: str) -> bool:
        """Execute _matches operation.

        Args:
            path: The path parameter.

        Returns:
            The result of the operation.
        """
        for p in self.config.path_prefixes:
            if not p:
                continue
            normalized = p if p.endswith("/") else f"{p}/"
            if path == p.rstrip("/") or path.startswith(normalized):
                return True
        return False

    def _cache_control_value(self) -> str:
        """Execute _cache_control_value operation.

        Returns:
            The result of the operation.
        """
        parts: list[str] = []
        if self.config.public:
            parts.append("public")
        parts.append(f"max-age={self.config.max_age_seconds}")
        parts.append("immutable")
        parts.extend(self.config.extra_directives)
        return ", ".join(parts)

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

        if request.method in {"GET", "HEAD"} and self._matches(request.url.path):
            response.headers[HEADER_CACHE_CONTROL] = self._cache_control_value()

        return response
