# HeaderTransformMiddleware

Transform request and response headers.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import HeaderTransformMiddleware

app = FastAPI()

app.add_middleware(
    HeaderTransformMiddleware,
    add_request_headers={"X-Custom": "value"},
    add_response_headers={"X-Powered-By": "FastMVC"},
    remove_response_headers={"Server"},
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `add_request_headers` | `dict[str, str]` | `{}` | Headers to add to requests |
| `add_response_headers` | `dict[str, str]` | `{}` | Headers to add to responses |
| `remove_request_headers` | `set[str]` | `set()` | Headers to remove from requests |
| `remove_response_headers` | `set[str]` | `set()` | Headers to remove from responses |
| `rename_request_headers` | `dict[str, str]` | `{}` | Headers to rename in requests |
| `rename_response_headers` | `dict[str, str]` | `{}` | Headers to rename in responses |

## Examples

### Add Response Headers

```python
app.add_middleware(
    HeaderTransformMiddleware,
    add_response_headers={
        "X-Powered-By": "FastMVC",
        "X-Content-Type-Options": "nosniff",
        "X-Request-Id": "{request_id}",
    },
)

```

### Remove Server Information

```python
app.add_middleware(
    HeaderTransformMiddleware,
    remove_response_headers={"Server", "X-Powered-By"},
)

```

### Add Request Headers

```python
app.add_middleware(
    HeaderTransformMiddleware,
    add_request_headers={
        "X-Forwarded-Proto": "https",
        "X-Internal-Request": "true",
    },
)

```

### Rename Headers

```python
app.add_middleware(
    HeaderTransformMiddleware,
    rename_request_headers={
        "X-Old-Header": "X-New-Header",
    },
    rename_response_headers={
        "X-Custom-Id": "X-Request-Id",
    },
)

```

### Dynamic Header Values

```python
from datetime import datetime

app.add_middleware(
    HeaderTransformMiddleware,
    add_response_headers={
        "X-Response-Time": "{response_time}",
        "X-Server-Time": lambda: datetime.utcnow().isoformat(),
    },
)

```

### Security Headers

```python
app.add_middleware(
    HeaderTransformMiddleware,
    add_response_headers={
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    },
    remove_response_headers={
        "Server",
        "X-Powered-By",
        "X-AspNet-Version",
    },
)

```

### CORS Headers

```python
app.add_middleware(
    HeaderTransformMiddleware,
    add_response_headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    },
)

```

### Caching Headers

```python
app.add_middleware(
    HeaderTransformMiddleware,
    add_response_headers={
        "Cache-Control": "public, max-age=3600",
        "Vary": "Accept-Encoding",
    },
)

```

## Use Cases

1. **Security Hardening** - Add security headers, remove server info
2. **Debugging** - Add request IDs, timing info
3. **Compatibility** - Rename headers for legacy clients
4. **CORS** - Add CORS headers globally

## Related Middlewares

- [SecurityHeadersMiddleware](security-headers.md) - Comprehensive security headers
- [CORSMiddleware](cors.md) - CORS configuration
- [RequestIDMiddleware](request-id.md) - Request ID generation
