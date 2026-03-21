# AuditMiddleware

Comprehensive audit logging for compliance and security tracking.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import AuditMiddleware

app = FastAPI()

app.add_middleware(
    AuditMiddleware,
    log_request_body=True,
    log_response_body=False,
    sensitive_headers={"Authorization", "Cookie"},
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `log_request_body` | `bool` | `False` | Log request body content |
| `log_response_body` | `bool` | `False` | Log response body content |
| `sensitive_headers` | `set[str]` | `{"Authorization"}` | Headers to redact |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip auditing |
| `max_body_size` | `int` | `10000` | Max body size to log (bytes) |

## Audit Log Format

```json
{
    "timestamp": "2025-01-18T10:30:45.123Z",
    "request_id": "abc-123-def",
    "event": "api_request",
    "method": "POST",
    "path": "/api/users",
    "client_ip": "192.168.1.100",
    "user_id": "user_123",
    "status_code": 201,
    "duration_ms": 45.2,
    "request_headers": {
        "Content-Type": "application/json",
        "Authorization": "[REDACTED]"
    },
    "request_body": {"name": "John", "email": "john@example.com"},
    "response_status": 201
}

```

## Examples

### Basic Audit Logging

```python
app.add_middleware(
    AuditMiddleware,
    log_request_body=True,
)

```

### Compliance-Ready Logging

```python
app.add_middleware(
    AuditMiddleware,
    log_request_body=True,
    log_response_body=True,
    sensitive_headers={"Authorization", "Cookie", "X-API-Key"},
    exclude_paths={"/health", "/metrics"},
)

```

### Custom Audit Handler

```python
from fastmiddleware import AuditMiddleware, AuditEvent

async def custom_audit_handler(event: AuditEvent):
    # Send to SIEM, database, or external service
    await send_to_splunk(event)

app.add_middleware(
    AuditMiddleware,
    handler=custom_audit_handler,
)

```

### With User Context

```python
from fastmiddleware import AuditMiddleware, RequestContextMiddleware

# Add context first to capture user info
app.add_middleware(RequestContextMiddleware)
app.add_middleware(AuditMiddleware)

```

## Use Cases

1. **Regulatory Compliance** - GDPR, HIPAA, SOC2 audit trails
2. **Security Monitoring** - Track suspicious activity
3. **Debugging** - Detailed request/response logging
4. **Analytics** - API usage patterns

## Related Middlewares

- [LoggingMiddleware](logging.md) - General request logging
- [DataMaskingMiddleware](data-masking.md) - Mask sensitive data
- [RequestLoggerMiddleware](request-logger.md) - Access log formats
