# ResponseCacheMiddleware

In-memory response caching with TTL support.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ResponseCacheMiddleware

app = FastAPI()

cache = ResponseCacheMiddleware(
    app,
    default_ttl=60,
    max_size=1000,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `default_ttl` | `int` | `60` | Default TTL in seconds |
| `max_size` | `int` | `1000` | Max cached responses |
| `path_ttls` | `dict[str, int]` | `{}` | Per-path TTLs |
| `methods` | `set[str]` | `{"GET"}` | Methods to cache |

## Methods

### `invalidate(path: str) -> None`

Invalidate a specific cache entry.

```python
cache.invalidate("/api/users/123")

```

### `clear() -> None`

Clear all cached responses.

```python
cache.clear()

```

### `get_stats() -> dict`

Get cache statistics.

```python
stats = cache.get_stats()

# {"hits": 1500, "misses": 300, "size": 850}

```

## Examples

### Basic Caching

```python
cache = ResponseCacheMiddleware(
    app,
    default_ttl=60,
    max_size=1000,
)

```

### Path-Specific TTLs

```python
cache = ResponseCacheMiddleware(
    app,
    default_ttl=60,
    path_ttls={
        "/api/config": 3600,       # 1 hour
        "/api/static": 86400,      # 24 hours
        "/api/realtime": 5,        # 5 seconds
    },
)

```

### Exclude Dynamic Paths

```python
cache = ResponseCacheMiddleware(
    app,
    default_ttl=60,
    exclude_paths={
        "/api/user",
        "/api/session",
        "/api/cart",
    },
)

```

### Cache Invalidation

```python
cache = ResponseCacheMiddleware(app, default_ttl=300)

@app.put("/api/users/{id}")
async def update_user(id: str, data: UserUpdate):
    user = await db.update_user(id, data)

    # Invalidate cached response
    cache.invalidate(f"/api/users/{id}")
    cache.invalidate("/api/users")

    return user

```

### With Monitoring

```python
@app.get("/admin/cache-stats")
async def cache_stats():
    return cache.get_stats()

@app.delete("/admin/cache")
async def clear_cache():
    cache.clear()
    return {"status": "cleared"}

```

### Conditional Caching

```python
from fastmiddleware import ResponseCacheMiddleware

class ConditionalCache(ResponseCacheMiddleware):
    def should_cache(self, request, response) -> bool:
        # Only cache successful responses
        if response.status_code != 200:
            return False

        # Don't cache if no-cache header
        if request.headers.get("Cache-Control") == "no-cache":
            return False

        return True

cache = ConditionalCache(app, default_ttl=60)

```

## Response Headers

```http
X-Cache: HIT
X-Cache-TTL: 45

```

or

```http
X-Cache: MISS

```

## Cache Key

Cache key is computed from:

- Request method

- Request path

- Query parameters (sorted)

- Vary headers (if configured)

## Use Cases

1. **API Responses** - Cache expensive computations
2. **Static Data** - Cache configuration, lookups
3. **Rate Limited APIs** - Cache external API responses
4. **Database Queries** - Reduce database load

## Related Middlewares

- [CacheMiddleware](cache.md) - HTTP caching headers
- [ETagMiddleware](etag.md) - ETag generation
- [RequestCoalescingMiddleware](request-coalescing.md) - Request coalescing
