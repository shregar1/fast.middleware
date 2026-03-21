# ConditionalRequestMiddleware

Handle If-None-Match and If-Modified-Since for efficient caching.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ConditionalRequestMiddleware

app = FastAPI()

app.add_middleware(ConditionalRequestMiddleware)

```

## How It Works

1. Client sends request with `If-None-Match` (ETag) or `If-Modified-Since` header
2. Middleware checks if resource has changed
3. If unchanged, returns `304 Not Modified` (no body)
4. If changed, returns full response with new ETag/Last-Modified

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `etag_header` | `str` | `"ETag"` | ETag response header name |
| `last_modified_header` | `str` | `"Last-Modified"` | Last-Modified header name |

## Examples

### Basic Usage

```python
app.add_middleware(ConditionalRequestMiddleware)

# First request:

# Response: 200 OK

# ETag: "abc123"

# Second request with If-None-Match: "abc123"

# Response: 304 Not Modified (no body)

```

### With ETag Middleware

```python
from fastmiddleware import ConditionalRequestMiddleware, ETagMiddleware

# Add ETag generation first
app.add_middleware(ETagMiddleware)

# Then conditional request handling
app.add_middleware(ConditionalRequestMiddleware)

```

### With Cache Middleware

```python
from fastmiddleware import (
    ConditionalRequestMiddleware,
    CacheMiddleware,
    ETagMiddleware,
)

app.add_middleware(ETagMiddleware)
app.add_middleware(ConditionalRequestMiddleware)
app.add_middleware(CacheMiddleware, max_age=3600)

```

### Custom Last-Modified

```python
from fastapi import Response
from datetime import datetime

@app.get("/article/{id}")
async def get_article(id: str, response: Response):
    article = await db.get_article(id)

    response.headers["Last-Modified"] = article.updated_at.strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    return article

```

## Request/Response Flow

### First Request

```text
Client -> GET /resource
Server -> 200 OK
         ETag: "v1-hash"
         Last-Modified: Sat, 18 Jan 2025 10:00:00 GMT
         Body: {...}

```

### Subsequent Request (Unchanged)

```text
Client -> GET /resource
          If-None-Match: "v1-hash"
Server -> 304 Not Modified
          (no body)

```

### Subsequent Request (Changed)

```text
Client -> GET /resource
          If-None-Match: "v1-hash"
Server -> 200 OK
          ETag: "v2-hash"
          Body: {...new content...}

```

## Benefits

1. **Reduced Bandwidth** - No body sent for unchanged resources
2. **Faster Responses** - 304 responses are tiny
3. **Client Cache Validation** - Clients can validate cached content

## Related Middlewares

- [ETagMiddleware](etag.md) - Generate ETags
- [CacheMiddleware](cache.md) - HTTP caching headers
- [ResponseCacheMiddleware](response-cache.md) - Server-side caching
