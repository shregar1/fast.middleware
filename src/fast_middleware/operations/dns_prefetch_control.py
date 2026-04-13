"""``X-DNS-Prefetch-Control`` — opt out of DNS prefetching for privacy-sensitive apps."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from starlette.requests import Request
from starlette.responses import Response

from fast_middleware.mw_core.base import FastMVCMiddleware


@dataclass
class DNSPrefetchControlConfig:
    r"""Browser hint for DNS prefetch behavior.

    Common values: ``\"off\"`` (disable), ``\"on\"`` (allow). See MDN for semantics.
    """

    value: str = "off"
    header_name: str = "X-DNS-Prefetch-Control"


class DNSPrefetchControlMiddleware(FastMVCMiddleware):
    """Set ``X-DNS-Prefetch-Control`` on all responses (default ``off``).

    Example::

        from fastmiddleware import DNSPrefetchControlMiddleware, DNSPrefetchControlConfig

        app.add_middleware(
            DNSPrefetchControlMiddleware,
            config=DNSPrefetchControlConfig(value="off"),
        )
    """

    def __init__(
        self,
        app,
        config: DNSPrefetchControlConfig | None = None,
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
        self.config = config or DNSPrefetchControlConfig()

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
        response.headers[self.config.header_name] = self.config.value
        return response
