"""Security-related HTTP response headers (HSTS, MIME sniffing, framing / CSP)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


@dataclass
class SecurityHeadersConfig:
    """Defaults favour safe framing and MIME handling; HSTS is opt-in (set ``hsts_max_age``)."""

    #: If True, set ``X-Content-Type-Options: nosniff``.
    x_content_type_options_nosniff: bool = True
    #: ``DENY``, ``SAMEORIGIN``, or None to omit ``X-Frame-Options``.
    x_frame_options: Optional[str] = "DENY"
    #: If set, add ``Content-Security-Policy: frame-ancestors <value>`` (e.g. ``"'none'"``, ``"'self'"``).
    csp_frame_ancestors: Optional[str] = "'none'"
    #: If set, send ``Strict-Transport-Security`` (HTTPS only in production).
    hsts_max_age: Optional[int] = None
    #: Append ``; includeSubDomains`` to HSTS when ``hsts_max_age`` is set.
    hsts_include_subdomains: bool = False


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Apply configurable security headers to every response.

    * ``X-Content-Type-Options: nosniff`` — reduces MIME confusion attacks.
    * ``X-Frame-Options`` — legacy clickjacking mitigation (pair with CSP when possible).
    * ``Content-Security-Policy: frame-ancestors …`` — modern control over embedding (optional).
    * ``Strict-Transport-Security`` — only when ``hsts_max_age`` is set (typical: 31536000).
    """

    def __init__(
        self,
        app,
        *,
        config: Optional[SecurityHeadersConfig] = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
        """
        super().__init__(app)
        self._config = config or SecurityHeadersConfig()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Execute dispatch operation.

        Args:
            request: The request parameter.
            call_next: The call_next parameter.

        Returns:
            The result of the operation.
        """
        response = await call_next(request)
        c = self._config

        if c.x_content_type_options_nosniff:
            response.headers["X-Content-Type-Options"] = "nosniff"

        if c.x_frame_options:
            response.headers["X-Frame-Options"] = c.x_frame_options

        if c.csp_frame_ancestors is not None:
            response.headers["Content-Security-Policy"] = (
                f"frame-ancestors {c.csp_frame_ancestors}"
            )

        if c.hsts_max_age is not None:
            hsts = f"max-age={c.hsts_max_age}"
            if c.hsts_include_subdomains:
                hsts += "; includeSubDomains"
            response.headers["Strict-Transport-Security"] = hsts

        return response
