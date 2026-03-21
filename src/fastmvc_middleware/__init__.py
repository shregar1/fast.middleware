"""
HTTP middleware for FastMVC / Starlette applications.

Request correlation IDs are stored via :mod:`fastmvc_core.utils.request_id_context`
so the same id is available in route handlers and downstream code.
"""

from .request_id import DEFAULT_REQUEST_ID_HEADER, RequestIDMiddleware
from .security_headers import SecurityHeadersConfig, SecurityHeadersMiddleware
from .timing import DEFAULT_RESPONSE_TIME_HEADER, ResponseTimingMiddleware

__version__ = "0.8.0"

__all__ = [
    "__version__",
    "DEFAULT_REQUEST_ID_HEADER",
    "DEFAULT_RESPONSE_TIME_HEADER",
    "RequestIDMiddleware",
    "ResponseTimingMiddleware",
    "SecurityHeadersConfig",
    "SecurityHeadersMiddleware",
]
