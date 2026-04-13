"""Real IP Middleware for FastMVC.

Extracts real client IP from various proxy headers.
"""

from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from dataclasses import dataclass, field

from starlette.requests import Request
from starlette.responses import Response

from fast_middleware.mw_core.base import FastMVCMiddleware
from fast_middleware.constants import *


_real_ip_ctx: ContextVar[str | None] = ContextVar(STATE_REAL_IP, default=None)


def get_real_ip() -> str | None:
    """Get real client IP."""
    return _real_ip_ctx.get()


@dataclass
class RealIPConfig:
    """Configuration for real IP middleware.

    Attributes:
        headers: Headers to check for real IP (in order).
        trusted_proxies: Trusted proxy IP addresses.

    """

    headers: list[str] = field(
        default_factory=lambda: [
            "CF-Connecting-IP",  # Cloudflare
            HEADER_X_REAL_IP,  # nginx
            "True-Client-IP",  # Akamai
            HEADER_X_FORWARDED_FOR,  # Standard
        ]
    )
    trusted_proxies: set[str] = field(default_factory=set)


class RealIPMiddleware(FastMVCMiddleware):
    """Middleware that extracts real client IP.

    Checks various proxy headers to find the real
    client IP address behind proxies and CDNs.

    Example:
        ```python
        from fastmiddleware import RealIPMiddleware, get_real_ip

        app.add_middleware(RealIPMiddleware)

        @app.get("/")
        async def handler():
            ip = get_real_ip()
            return {"your_ip": ip}
        ```

    """

    def __init__(
        self,
        app,
        config: RealIPConfig | None = None,
        headers: list[str] | None = None,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            headers: The headers parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or RealIPConfig()

        if headers:
            self.config.headers = headers

    def _get_real_ip(self, request: Request) -> str:
        """Get real client IP from headers."""
        for header in self.config.headers:
            value = request.headers.get(header)
            if value:
                # X-Forwarded-For can contain multiple IPs
                ip = value.split(",")[0].strip() if "," in value else value.strip()

                if ip:
                    return ip

        # Fall back to direct connection IP
        client = request.scope.get("client")
        return client[0] if client else DEFAULT_UNKNOWN

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

        real_ip = self._get_real_ip(request)

        token = _real_ip_ctx.set(real_ip)
        request.state.real_ip = real_ip

        try:
            response = await call_next(request)
            return response
        finally:
            _real_ip_ctx.reset(token)
