"""Request Logger Middleware for FastMVC.

Logs requests in various formats.
"""

import json
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from starlette.requests import Request
from starlette.responses import Response

from fastx_middleware.mw_core.base import FastMVCMiddleware
from fastx_middleware.constants import *


@dataclass
class RequestLoggerConfig:
    """Configuration for request logger middleware.

    Attributes:
        format: Log format (combined, common, json, custom).
        logger_name: Logger name.
        log_level: Log level.
        include_headers: Include headers in log.
        mask_headers: Headers to mask values.
        skip_paths: Paths to skip logging.

    """

    format: str = LOG_FORMAT_COMBINED
    logger_name: str = LOGGER_ACCESS
    log_level: int = logging.INFO
    include_headers: bool = False
    mask_headers: set[str] = field(
        default_factory=lambda: {HEADER_AUTHORIZATION, HEADER_COOKIE, HEADER_X_API_KEY}
    )
    skip_paths: set[str] = field(
        default_factory=lambda: {"/health", "/ready", "/metrics"}
    )


class RequestLoggerMiddleware(FastMVCMiddleware):
    """Middleware for logging requests.

    Logs HTTP requests in various formats including
    Apache Combined, Common, and JSON.

    Example:
        ```python
        from fastmiddleware import RequestLoggerMiddleware

        app.add_middleware(
            RequestLoggerMiddleware,
            format="json",
            skip_paths={"/health"},
        )
        ```

    """

    def __init__(
        self,
        app,
        config: RequestLoggerConfig | None = None,
        format: str | None = None,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            format: The format parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or RequestLoggerConfig()

        if format:
            self.config.format = format

        self._logger = logging.getLogger(self.config.logger_name)

    def _mask_value(self, value: str) -> str:
        """Mask sensitive value."""
        if len(value) <= 4:
            return "***"
        return value[:2] + "***" + value[-2:]

    def _format_combined(
        self, request: Request, response: Response, duration: float
    ) -> str:
        """Format in Apache Combined format."""
        client_ip = self.get_client_ip(request)
        timestamp = datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S %z")
        method = request.method
        path = request.url.path
        if request.url.query:
            path += f"?{request.url.query}"
        protocol = f"HTTP/{request.scope.get('http_version', '1.1')}"
        status = response.status_code
        size = response.headers.get("content-length", "-")
        referer = request.headers.get(HEADER_REFERER, "-")
        user_agent = request.headers.get(HEADER_USER_AGENT, "-")

        return (
            f'{client_ip} - - [{timestamp}] "{method} {path} {protocol}" '
            f'{status} {size} "{referer}" "{user_agent}" {duration:.3f}s'
        )

    def _format_common(
        self, request: Request, response: Response, duration: float
    ) -> str:
        """Format in Apache Common format."""
        client_ip = self.get_client_ip(request)
        timestamp = datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S %z")
        method = request.method
        path = request.url.path
        protocol = f"HTTP/{request.scope.get('http_version', '1.1')}"
        status = response.status_code
        size = response.headers.get("content-length", "-")

        return f'{client_ip} - - [{timestamp}] "{method} {path} {protocol}" {status} {size}'

    def _format_json(
        self, request: Request, response: Response, duration: float
    ) -> str:
        """Format as JSON."""
        data: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            STATE_CLIENT_IP: self.get_client_ip(request),
            "method": request.method,
            "path": request.url.path,
            "query": str(request.url.query) if request.url.query else None,
            "status": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "user_agent": request.headers.get(HEADER_USER_AGENT),
            "referer": request.headers.get(HEADER_REFERER),
        }

        if self.config.include_headers:
            headers = {}
            for name, value in request.headers.items():
                if name in self.config.mask_headers:
                    headers[name] = self._mask_value(value)
                else:
                    headers[name] = value
            data["headers"] = headers

        return json.dumps(data)

    def _format(self, request: Request, response: Response, duration: float) -> str:
        """Format log entry."""
        if self.config.format == "json":
            return self._format_json(request, response, duration)
        elif self.config.format == LOG_FORMAT_COMMON:
            return self._format_common(request, response, duration)
        else:  # combined
            return self._format_combined(request, response, duration)

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
        if request.url.path in self.config.skip_paths:
            return await call_next(request)

        if self.should_skip(request):
            return await call_next(request)

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        log_line = self._format(request, response, duration)
        self._logger.log(self.config.log_level, log_line)

        return response
