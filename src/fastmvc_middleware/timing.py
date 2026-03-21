"""
``X-Response-Time`` header: wall-clock duration to produce the response.
"""

from __future__ import annotations

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

DEFAULT_RESPONSE_TIME_HEADER = "X-Response-Time"


class ResponseTimingMiddleware(BaseHTTPMiddleware):
    """
    Add ``X-Response-Time`` with elapsed seconds (floating point, 6 decimal places).

    Measured with :func:`time.perf_counter` around the downstream ASGI call.
    """

    def __init__(
        self,
        app,
        *,
        header_name: str = DEFAULT_RESPONSE_TIME_HEADER,
        unit_seconds: bool = True,
    ) -> None:
        super().__init__(app)
        self.header_name = header_name
        self.unit_seconds = unit_seconds

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        t0 = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - t0
        if self.unit_seconds:
            response.headers[self.header_name] = f"{elapsed:.6f}"
        else:
            response.headers[self.header_name] = f"{elapsed * 1000:.3f}"
        return response
