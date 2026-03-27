"""Response compression preset wrapping Starlette :class:`GZipMiddleware`.

Brotli is not provided by Starlette; terminate compression at your CDN or ASGI server
if you need brotli.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from starlette.middleware.gzip import GZipMiddleware


class CompressionPreset(BaseModel):
    """Opt-in gzip for JSON/HTML-heavy responses (Starlette ``GZipMiddleware``).

    ``minimum_size`` avoids compressing tiny payloads where overhead dominates.
    """

    enabled: bool = True
    minimum_size: int = Field(
        default=500, ge=0, description="Minimum response bytes to gzip."
    )

    def add_to_app(self, app) -> None:
        """Register gzip middleware on *app* when *enabled*."""
        if self.enabled:
            app.add_middleware(GZipMiddleware, minimum_size=self.minimum_size)
