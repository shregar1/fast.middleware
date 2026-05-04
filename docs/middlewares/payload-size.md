# PayloadSizeMiddleware

Limit request and response payload sizes.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import PayloadSizeMiddleware

app = FastAPI()

app.add_middleware(
    PayloadSizeMiddleware,
    max_request_size=10 * 1024 * 1024,   # 10 MB
    max_response_size=50 * 1024 * 1024,  # 50 MB
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `max_request_size` | `int` | `10485760` | Max request body (10 MB) |
| `max_response_size` | `int` | `None` | Max response body (unlimited) |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip validation |

## Examples

### Limit Request Size

```python
app.add_middleware(
    PayloadSizeMiddleware,
    max_request_size=5 * 1024 * 1024,  # 5 MB
)

# Request > 5 MB → 413 Payload Too Large

```

### Limit Both Directions

```python
app.add_middleware(
    PayloadSizeMiddleware,
    max_request_size=10 * 1024 * 1024,   # 10 MB requests
    max_response_size=100 * 1024 * 1024,  # 100 MB responses
)

```

### Exclude Upload Endpoints

```python
app.add_middleware(
    PayloadSizeMiddleware,
    max_request_size=1 * 1024 * 1024,  # 1 MB default
    exclude_paths={"/api/upload", "/api/import"},
)

```

### Path-Specific Limits

```python

# Use multiple middlewares or custom logic
from fastmiddleware import PayloadSizeMiddleware

class PathAwarePayloadSize(PayloadSizeMiddleware):
    def get_limit(self, path: str) -> int:
        limits = {
            "/api/upload": 100 * 1024 * 1024,  # 100 MB
            "/api/import": 50 * 1024 * 1024,   # 50 MB
        }
        return limits.get(path, self.max_request_size)

app.add_middleware(
    PathAwarePayloadSize,
    max_request_size=5 * 1024 * 1024,
)

```

### Content-Type Specific

```python
class ContentAwarePayloadSize(PayloadSizeMiddleware):
    def get_limit(self, request) -> int:
        content_type = request.headers.get("content-type", "")

        if "multipart/form-data" in content_type:
            return 50 * 1024 * 1024  # 50 MB for uploads
        elif "application/json" in content_type:
            return 1 * 1024 * 1024   # 1 MB for JSON

        return self.max_request_size

app.add_middleware(ContentAwarePayloadSize, max_request_size=5 * 1024 * 1024)

```

## Error Response

```json
{
    "error": "Payload Too Large",
    "detail": "Request body exceeds maximum size of 10485760 bytes",
    "status_code": 413
}

```

## Use Cases

1. **DDoS Prevention** - Limit large payload attacks
2. **Resource Control** - Prevent memory exhaustion
3. **API Contracts** - Enforce size limits
4. **Storage Limits** - Match storage quotas

## Related Middlewares

- [RequestLimitMiddleware](request-limit.md) - Request body limits
- [CompressionMiddleware](compression.md) - Response compression
- [RateLimitMiddleware](rate-limit.md) - Rate limiting
