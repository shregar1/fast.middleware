"""Response compression preset wrapping Starlette :class:`GZipMiddleware`.

Brotli is not provided by Starlette; terminate compression at your CDN or ASGI server
if you need brotli.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from starlette.middleware.gzip import GZipMiddleware

from fastx_middleware.constants import DEFAULT_MIN_GZIP_SIZE


class CompressionConfig(BaseModel):
    """Structured options for :class:`CompressionMiddleware` (legacy test / API surface).

    ``compression_level`` is accepted for compatibility; Starlette gzip uses zlib defaults.
    """

    minimum_size: int = Field(default=500, ge=0)
    compression_level: int = Field(default=6, ge=1, le=9)
    compressible_types: tuple[str, ...] = Field(
        default=(
            "application/json",
            "text/html",
            "text/css",
            "text/plain",
            "application/javascript",
        )
    )


class CompressionMiddleware:
    """HTTP gzip middleware with optional path exclusion.

    Wraps Starlette :class:`~starlette.middleware.gzip.GZipMiddleware`.
    """

    def __init__(
        self,
        app: Any,
        *,
        minimum_size: int = DEFAULT_MIN_GZIP_SIZE,
        exclude_paths: frozenset[str] | set[str] | None = None,
        config: CompressionConfig | None = None,
        **kwargs: Any,
    ) -> None:
        if config is not None:
            minimum_size = config.minimum_size
        self._app = app
        self._exclude_paths = frozenset(exclude_paths or ())
        self._gzip = GZipMiddleware(app, minimum_size=minimum_size)

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        if (
            scope.get("type") == "http"
            and self._exclude_paths
            and scope.get("path") in self._exclude_paths
        ):
            await self._app(scope, receive, send)
            return
        await self._gzip(scope, receive, send)


class CompressionPreset(BaseModel):
    """Opt-in gzip for JSON/HTML-heavy responses (Starlette ``GZipMiddleware``).

    ``minimum_size`` avoids compressing tiny payloads where overhead dominates.
    """

    enabled: bool = True
    minimum_size: int = Field(
        default=DEFAULT_MIN_GZIP_SIZE, ge=0, description="Minimum response bytes to gzip."
    )

    def add_to_app(self, app) -> None:
        """Register gzip middleware on *app* when *enabled*."""
        if self.enabled:
            app.add_middleware(GZipMiddleware, minimum_size=self.minimum_size)
