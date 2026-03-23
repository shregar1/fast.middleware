"""
Resolve the client IP behind reverse proxies (``X-Forwarded-For``, ``X-Real-IP``).
"""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

STATE_CLIENT_IP = "fast_client_ip"


def get_client_ip(
    request: Request,
    *,
    trusted_proxy_depth: int = 1,
    use_x_real_ip: bool = True,
) -> str:
    """
    Best-effort client IP for logging and rate limiting.

    * **trusted_proxy_depth** — Number of trusted proxies in front of the app. When
      ``X-Forwarded-For`` is present, the **leftmost** address is treated as the original
      client if ``depth >= 1`` (typical: one load balancer or ingress). Set ``0`` to
      ignore ``X-Forwarded-For`` and use the TCP peer only (safe when not behind a proxy).
    * **use_x_real_ip** — If True, fall back to ``X-Real-IP`` when ``X-Forwarded-For`` is absent.

    The TCP peer from ASGI (``request.client.host``) is used when headers do not apply.
    """
    if trusted_proxy_depth > 0:
        xff = request.headers.get("x-forwarded-for") or request.headers.get("X-Forwarded-For")
        if xff:
            parts = [p.strip() for p in xff.split(",") if p.strip()]
            if parts:
                return parts[0]
        if use_x_real_ip:
            xr = request.headers.get("x-real-ip") or request.headers.get("X-Real-IP")
            if xr:
                return xr.strip()
    if request.client and request.client.host:
        return request.client.host
    return "0.0.0.0"


class ClientIPMiddleware(BaseHTTPMiddleware):
    """
    Store :func:`get_client_ip` on ``request.state`` for handlers and downstream middleware.

    Uses attribute name :data:`STATE_CLIENT_IP` (``\"fast_client_ip\"``).
    """

    def __init__(
        self,
        app,
        *,
        trusted_proxy_depth: int = 1,
        use_x_real_ip: bool = True,
    ) -> None:
        super().__init__(app)
        self.trusted_proxy_depth = trusted_proxy_depth
        self.use_x_real_ip = use_x_real_ip

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        ip = get_client_ip(
            request,
            trusted_proxy_depth=self.trusted_proxy_depth,
            use_x_real_ip=self.use_x_real_ip,
        )
        setattr(request.state, STATE_CLIENT_IP, ip)
        return await call_next(request)


def read_client_ip(request: Request) -> str | None:
    """Return ``request.state.fast_client_ip`` if :class:`ClientIPMiddleware` ran."""
    return getattr(request.state, STATE_CLIENT_IP, None)
