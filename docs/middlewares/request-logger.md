# RequestLoggerMiddleware

Access logging in various standard formats.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestLoggerMiddleware

app = FastAPI()

app.add_middleware(
    RequestLoggerMiddleware,
    format="combined",
    skip_paths={"/health", "/metrics"},
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `format` | `str` | `"combined"` | Log format |
| `skip_paths` | `set[str]` | `set()` | Paths to skip logging |
| `logger` | `Logger` | `None` | Custom logger instance |

## Log Formats

### Combined (Apache)

```text
192.168.1.100 - john [18/Jan/2025:10:30:00 +0000] "GET /api/users HTTP/1.1" 200 1234 "https://example.com" "Mozilla/5.0..."

```

### Common (Apache)

```text
192.168.1.100 - john [18/Jan/2025:10:30:00 +0000] "GET /api/users HTTP/1.1" 200 1234

```

### JSON

```json
{
    "timestamp": "2025-01-18T10:30:00Z",
    "client_ip": "192.168.1.100",
    "method": "GET",
    "path": "/api/users",
    "status": 200,
    "size": 1234,
    "duration_ms": 45.2,
    "user_agent": "Mozilla/5.0..."
}

```

## Examples

### Combined Format

```python
app.add_middleware(
    RequestLoggerMiddleware,
    format="combined",
)

```

### JSON Format

```python
app.add_middleware(
    RequestLoggerMiddleware,
    format="json",
)

```

### Skip Health Checks

```python
app.add_middleware(
    RequestLoggerMiddleware,
    format="combined",
    skip_paths={"/health", "/ready", "/live", "/metrics"},
)

```

### Custom Logger

```python
import logging

access_logger = logging.getLogger("access")
access_logger.setLevel(logging.INFO)
handler = logging.FileHandler("access.log")
access_logger.addHandler(handler)

app.add_middleware(
    RequestLoggerMiddleware,
    format="combined",
    logger=access_logger,
)

```

### With Request ID

```python
from fastmiddleware import RequestLoggerMiddleware, RequestIDMiddleware

# Request ID first
app.add_middleware(RequestIDMiddleware)

# Logger includes request ID
app.add_middleware(
    RequestLoggerMiddleware,
    format="json",
)

```

### Filter by Status Code

```python
from fastmiddleware import RequestLoggerMiddleware

class ErrorOnlyLogger(RequestLoggerMiddleware):
    def should_log(self, request, response) -> bool:
        return response.status_code >= 400

app.add_middleware(ErrorOnlyLogger, format="json")

```

## Format Reference

| Token | Description |
| ------- | ------------- |
| `%h` | Remote host |
| `%l` | Remote logname (always -) |
| `%u` | Remote user |
| `%t` | Time in CLF format |
| `%r` | First line of request |
| `%s` | Status code |
| `%b` | Response size |
| `%{Referer}i` | Referer header |
| `%{User-Agent}i` | User-Agent header |
| `%D` | Request duration (microseconds) |

## Related Middlewares

- [LoggingMiddleware](logging.md) - Structured logging
- [AuditMiddleware](audit.md) - Audit logging
- [MetricsMiddleware](metrics.md) - Prometheus metrics
