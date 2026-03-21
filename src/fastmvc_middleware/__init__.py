"""
HTTP middleware for FastMVC / Starlette applications.

Request correlation IDs are stored via :mod:`fastmvc_core.utils.request_id_context`
so the same id is available in route handlers and downstream code.

Also: CORS preset DTO, body-size guard, client IP helpers, gzip compression preset.
"""

from .body_limit import BodySizeLimitMiddleware
from .client_ip import (
    STATE_CLIENT_IP,
    ClientIPMiddleware,
    get_client_ip,
    read_client_ip,
)
from .compression import CompressionPreset
from .cors_preset import CORSPreset
from .request_id import DEFAULT_REQUEST_ID_HEADER, RequestIDMiddleware
from .security_headers import SecurityHeadersConfig, SecurityHeadersMiddleware
from .timing import DEFAULT_RESPONSE_TIME_HEADER, ResponseTimingMiddleware

__version__ = "0.9.0"

__all__ = [
    "__version__",
    "BodySizeLimitMiddleware",
    "ClientIPMiddleware",
    "CompressionPreset",
    "CORSPreset",
    "DEFAULT_REQUEST_ID_HEADER",
    "DEFAULT_RESPONSE_TIME_HEADER",
    "RequestIDMiddleware",
    "ResponseTimingMiddleware",
    "SecurityHeadersConfig",
    "SecurityHeadersMiddleware",
    "STATE_CLIENT_IP",
    "get_client_ip",
    "read_client_ip",
]
