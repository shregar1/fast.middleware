# RequestLimitMiddleware

Limit request body size.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestLimitMiddleware

app = FastAPI()

app.add_middleware(
    RequestLimitMiddleware,
    max_size=10 * 1024 * 1024,  # 10 MB
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `max_size` | `int` | `10485760` | Max body size (10 MB) |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip |

## Examples

### Basic Size Limit

```python
app.add_middleware(
    RequestLimitMiddleware,
    max_size=5 * 1024 * 1024,  # 5 MB
)

```

### Small JSON Limit

```python
app.add_middleware(
    RequestLimitMiddleware,
    max_size=1 * 1024 * 1024,  # 1 MB for JSON APIs
)

```

### Exclude Upload Paths

```python
app.add_middleware(
    RequestLimitMiddleware,
    max_size=1 * 1024 * 1024,  # 1 MB default
    exclude_paths={"/upload", "/import"},
)

```

### Multiple Limits (Custom)

```python
from fastmiddleware import RequestLimitMiddleware

class PathAwareLimit(RequestLimitMiddleware):
    def get_limit(self, request) -> int:
        if request.url.path.startswith("/upload"):
            return 100 * 1024 * 1024  # 100 MB
        elif request.url.path.startswith("/api"):
            return 1 * 1024 * 1024    # 1 MB
        return self.max_size

app.add_middleware(PathAwareLimit, max_size=5 * 1024 * 1024)

```

## Error Response

```json
{
    "error": "Request Entity Too Large",
    "detail": "Request body exceeds maximum size of 10485760 bytes",
    "status_code": 413
}

```

## Use Cases

1. **DDoS Protection** - Prevent large payload attacks
2. **Resource Management** - Control memory usage
3. **API Contracts** - Enforce payload limits
4. **Cost Control** - Limit bandwidth usage

## Related Middlewares

- [PayloadSizeMiddleware](payload-size.md) - Request and response limits
- [ContentTypeMiddleware](content-type.md) - Content-Type validation
- [TimeoutMiddleware](timeout.md) - Request timeouts
