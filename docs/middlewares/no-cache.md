# NoCacheMiddleware

Disable caching for specific paths or all responses.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import NoCacheMiddleware

app = FastAPI()

app.add_middleware(
    NoCacheMiddleware,
    paths={"/api/user", "/api/session"},
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `paths` | `set[str]` | `set()` | Paths to disable caching |
| `apply_all` | `bool` | `False` | Apply to all responses |

## Response Headers

```http
Cache-Control: no-cache, no-store, must-revalidate, private
Pragma: no-cache
Expires: 0

```

## Examples

### Specific Paths

```python
app.add_middleware(
    NoCacheMiddleware,
    paths={
        "/api/user",
        "/api/session",
        "/api/cart",
        "/api/checkout",
    },
)

```

### All Responses

```python
app.add_middleware(
    NoCacheMiddleware,
    apply_all=True,
)

```

### Path Patterns

```python
app.add_middleware(
    NoCacheMiddleware,
    paths={
        "/api/user/*",     # Wildcard
        "/api/private/*",
    },
)

```

### Combine with Cache Middleware

```python
from fastmiddleware import CacheMiddleware, NoCacheMiddleware

# No cache for sensitive endpoints
app.add_middleware(
    NoCacheMiddleware,
    paths={"/api/user", "/api/admin"},
)

# Cache for everything else
app.add_middleware(
    CacheMiddleware,
    max_age=3600,
)

```

### Dynamic Content

```python
app.add_middleware(
    NoCacheMiddleware,
    paths={
        "/api/realtime",
        "/api/notifications",
        "/api/feed",
    },
)

```

## Use Cases

1. **User Data** - Prevent caching sensitive user information
2. **Session Data** - Ensure session state is always fresh
3. **Real-time Data** - Stock prices, live feeds
4. **Auth Endpoints** - Login, logout, token refresh

## Related Middlewares

- [CacheMiddleware](cache.md) - HTTP caching headers
- [ResponseCacheMiddleware](response-cache.md) - Server-side caching
- [ETagMiddleware](etag.md) - ETag generation
