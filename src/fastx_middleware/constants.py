"""Shared constants for fastx_middleware to avoid magic strings/numbers."""

from __future__ import annotations

from typing import Final

# HTTP status codes
HTTP_200_OK: Final[int] = 200
HTTP_204_NO_CONTENT: Final[int] = 204
HTTP_301_MOVED_PERMANENTLY: Final[int] = 301
HTTP_302_FOUND: Final[int] = 302
HTTP_304_NOT_MODIFIED: Final[int] = 304
HTTP_308_PERMANENT_REDIRECT: Final[int] = 308
HTTP_400_BAD_REQUEST: Final[int] = 400
HTTP_401_UNAUTHORIZED: Final[int] = 401
HTTP_403_FORBIDDEN: Final[int] = 403
HTTP_404_NOT_FOUND: Final[int] = 404
HTTP_406_NOT_ACCEPTABLE: Final[int] = 406
HTTP_412_PRECONDITION_FAILED: Final[int] = 412
HTTP_413_PAYLOAD_TOO_LARGE: Final[int] = 413
HTTP_415_UNSUPPORTED_MEDIA_TYPE: Final[int] = 415
HTTP_429_TOO_MANY_REQUESTS: Final[int] = 429
HTTP_500_INTERNAL_SERVER_ERROR: Final[int] = 500
HTTP_502_BAD_GATEWAY: Final[int] = 502
HTTP_503_SERVICE_UNAVAILABLE: Final[int] = 503
HTTP_504_GATEWAY_TIMEOUT: Final[int] = 504

# Headers
HEADER_CONTENT_TYPE: Final[str] = "Content-Type"
HEADER_CONTENT_LENGTH: Final[str] = "Content-Length"
HEADER_USER_AGENT: Final[str] = "User-Agent"
HEADER_AUTHORIZATION: Final[str] = "Authorization"
HEADER_ACCEPT: Final[str] = "Accept"
HEADER_ACCEPT_LANGUAGE: Final[str] = "Accept-Language"
HEADER_ACCEPT_ENCODING: Final[str] = "Accept-Encoding"
HEADER_X_REQUEST_ID: Final[str] = "X-Request-ID"
HEADER_X_FORWARDED_FOR: Final[str] = "X-Forwarded-For"
HEADER_X_REAL_IP: Final[str] = "X-Real-IP"
HEADER_REFERER: Final[str] = "Referer"
HEADER_COOKIE: Final[str] = "Cookie"
HEADER_HOST: Final[str] = "Host"
HEADER_X_API_KEY: Final[str] = "X-API-Key"
HEADER_X_CORRELATION_ID: Final[str] = "X-Correlation-ID"
HEADER_X_TRACE_ID: Final[str] = "X-Trace-ID"
HEADER_IF_NONE_MATCH: Final[str] = "If-None-Match"
HEADER_IF_MATCH: Final[str] = "If-Match"
HEADER_IF_MODIFIED_SINCE: Final[str] = "If-Modified-Since"
HEADER_LAST_MODIFIED: Final[str] = "Last-Modified"
HEADER_ETAG: Final[str] = "ETag"
HEADER_CACHE_CONTROL: Final[str] = "Cache-Control"
HEADER_VARY: Final[str] = "Vary"
HEADER_PRAGMA: Final[str] = "Pragma"
HEADER_EXPIRES: Final[str] = "Expires"
HEADER_SERVER: Final[str] = "Server"
HEADER_ORIGIN: Final[str] = "Origin"
HEADER_WWW_AUTHENTICATE: Final[str] = "WWW-Authenticate"
HEADER_RETRY_AFTER: Final[str] = "Retry-After"
HEADER_SERVER_TIMING: Final[str] = "Server-Timing"
HEADER_X_LOAD_SHEDDING: Final[str] = "X-Load-Shedding"
HEADER_X_MAINTENANCE_MODE: Final[str] = "X-Maintenance-Mode"
HEADER_X_RATELIMIT_LIMIT: Final[str] = "X-RateLimit-Limit"
HEADER_X_RATELIMIT_REMAINING: Final[str] = "X-RateLimit-Remaining"
HEADER_X_RATELIMIT_RESET: Final[str] = "X-RateLimit-Reset"
HEADER_X_FORWARDED_PROTO: Final[str] = "X-Forwarded-Proto"
HEADER_X_FORWARDED_HOST: Final[str] = "X-Forwarded-Host"
HEADER_X_POWERED_BY: Final[str] = "X-Powered-By"
HEADER_X_FRAME_OPTIONS: Final[str] = "X-Frame-Options"

# Content types
CONTENT_TYPE_JSON: Final[str] = "application/json"
CONTENT_TYPE_HTML: Final[str] = "text/html"
CONTENT_TYPE_PLAIN: Final[str] = "text/plain"
CONTENT_TYPE_XML: Final[str] = "application/xml"
CONTENT_TYPE_MULTIPART: Final[str] = "multipart/form-data"
CONTENT_TYPE_FORM_URLENCODED: Final[str] = "application/x-www-form-urlencoded"

# Error messages
MSG_AUTHENTICATION_REQUIRED: Final[str] = "Authentication required"
MSG_ACCESS_DENIED: Final[str] = "Access denied"
MSG_BOT_ACCESS_DENIED: Final[str] = "Bot access denied"
MSG_SERVICE_UNAVAILABLE: Final[str] = "Service temporarily unavailable"
MSG_INVALID_JSON: Final[str] = "Invalid JSON"
MSG_PAYLOAD_TOO_LARGE: Final[str] = "Request payload too large"
MSG_NOT_ACCEPTABLE: Final[str] = "Not Acceptable"
MSG_NOT_FOUND: Final[str] = "Not found"
MSG_RATE_LIMIT_EXCEEDED: Final[str] = "Rate limit exceeded. Please try again later."
MSG_QUOTA_EXCEEDED: Final[str] = "Quota exceeded"
DEFAULT_UNKNOWN: Final[str] = "unknown"

# Time constants (seconds)
DEFAULT_TIMEOUT_SECONDS: Final[float] = 30.0
DEFAULT_TIMEOUT_60S: Final[float] = 60.0
FIVE_MINUTES_SECONDS: Final[int] = 300
CORS_MAX_AGE_DEFAULT: Final[int] = 600
ONE_HOUR_SECONDS: Final[int] = 3600
ONE_DAY_SECONDS: Final[int] = 86400
DEFAULT_RETRY_AFTER_SECONDS: Final[float] = 5.0
DEFAULT_COALESCE_WINDOW: Final[float] = 0.1

# Size constants
BYTES_PER_MIB: Final[int] = 1024 * 1024
DEFAULT_MAX_BODY_BYTES: Final[int] = 1_048_576
DEFAULT_CHUNK_SIZE_BYTES: Final[int] = 8192
DEFAULT_MIN_GZIP_SIZE: Final[int] = 500
SLOW_REQUEST_THRESHOLD_MS: Final[int] = 500
DEFAULT_MAX_ENTRIES: Final[int] = 1000
DEFAULT_LIMIT_100: Final[int] = 100
DEFAULT_LIMIT_50: Final[int] = 50
DEFAULT_MAX_NONCE_CACHE: Final[int] = 10000
DEFAULT_MAX_STRING_LENGTH: Final[int] = 10000
DEFAULT_MAX_CHAIN_LENGTH: Final[int] = 10

# State attribute names
STATE_REQUEST_ID: Final[str] = "request_id"
STATE_USER: Final[str] = "user"
STATE_AUTH: Final[str] = "auth"
STATE_REAL_IP: Final[str] = "real_ip"
STATE_CLIENT_IP: Final[str] = "client_ip"
STATE_FEATURE_FLAGS: Final[str] = "feature_flags"
STATE_LOCALE: Final[str] = "locale"
STATE_TENANT: Final[str] = "tenant"
STATE_TENANT_ID: Final[str] = "tenant_id"
STATE_CORRELATION_ID: Final[str] = "correlation_id"
STATE_FINGERPRINT: Final[str] = "fingerprint"
STATE_GEO: Final[str] = "geo"
STATE_SESSION: Final[str] = "session"
STATE_PRIORITY: Final[str] = "priority"
STATE_IS_BOT: Final[str] = "is_bot"
STATE_START_TIME: Final[str] = "start_time"
STATE_CONTEXT: Final[str] = "context"

# Loggers
LOGGER_FASTMVC: Final[str] = "fastmvc.middleware"
LOGGER_FASTMVC_ERROR: Final[str] = "fastmvc.middleware.error"
LOGGER_ACCESS: Final[str] = "access"
LOGGER_EXCEPTIONS: Final[str] = "exceptions"
LOGGER_AUDIT: Final[str] = "audit"
LOGGER_CSP: Final[str] = "csp_reports"
LOGGER_HONEYPOT: Final[str] = "honeypot"
LOGGER_RESPONSE_TIME: Final[str] = "response_time"

# Field names
FIELD_ERROR: Final[str] = "error"
FIELD_MESSAGE: Final[str] = "message"
FIELD_DETAIL: Final[str] = "detail"

# Algorithms
ALGORITHM_MD5: Final[str] = "md5"
ALGORITHM_SHA1: Final[str] = "sha1"
ALGORITHM_SHA256: Final[str] = "sha256"
ALGORITHM_SHA512: Final[str] = "sha512"

# Rate limit strategies
RATE_LIMIT_STRATEGY_SLIDING: Final[str] = "sliding"
RATE_LIMIT_STRATEGY_FIXED: Final[str] = "fixed"
RATE_LIMIT_STRATEGY_TOKEN_BUCKET: Final[str] = "token_bucket"

# SameSite values
SAMESITE_LAX: Final[str] = "lax"
SAMESITE_STRICT: Final[str] = "strict"
SAMESITE_NONE: Final[str] = "none"

# Log formats
LOG_FORMAT_COMBINED: Final[str] = "combined"
LOG_FORMAT_COMMON: Final[str] = "common"
LOG_FORMAT_JSON: Final[str] = "json"
