"""
Reject oversized request bodies using ``Content-Length`` (DoS guard).

Chunked uploads without ``Content-Length`` are not pre-checked; add a reverse-proxy
limit or stream-read guard separately for those paths.
"""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    """
    Return ``413 Payload Too Large`` when ``Content-Length`` exceeds *max_bytes*.

    Only inspects the ``Content-Length`` header; missing header allows the request
    (typical for GET or small bodies). For large chunked bodies, terminate at the proxy.
    """

    def __init__(self, app, *, max_bytes: int = 1_048_576) -> None:
        super().__init__(app)
        if max_bytes < 0:
            raise ValueError("max_bytes must be non-negative")
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        raw = request.headers.get("content-length")
        if raw is not None:
            try:
                length = int(raw)
            except ValueError:
                return JSONResponse(
                    {"detail": "Invalid Content-Length"},
                    status_code=400,
                )
            if length > self.max_bytes:
                return JSONResponse(
                    {"detail": f"Request body exceeds maximum of {self.max_bytes} bytes"},
                    status_code=413,
                )
        return await call_next(request)
