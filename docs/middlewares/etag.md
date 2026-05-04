# ETagMiddleware

Generate and validate ETags for response caching.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ETagMiddleware

app = FastAPI()

app.add_middleware(ETagMiddleware)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `weak` | `bool` | `True` | Use weak ETags (W/"...") |
| `hash_algorithm` | `str` | `"md5"` | Hash algorithm for ETag |

## How It Works

1. Response body is hashed to generate ETag
2. ETag header is added to response
3. On subsequent requests with `If-None-Match`, ETag is validated
4. Returns 304 Not Modified if unchanged

## Examples

### Basic ETag Generation

```python
app.add_middleware(ETagMiddleware)

# Response includes:

# ETag: W/"5d41402abc4b2a76b9719d911017c592"

```

### Strong ETags

```python
app.add_middleware(
    ETagMiddleware,
    weak=False,
)

# Response includes:

# ETag: "5d41402abc4b2a76b9719d911017c592"

```

### Custom Hash Algorithm

```python
app.add_middleware(
    ETagMiddleware,
    hash_algorithm="sha256",
)

```

### With Conditional Requests

```python
from fastmiddleware import ETagMiddleware, ConditionalRequestMiddleware

app.add_middleware(ETagMiddleware)
app.add_middleware(ConditionalRequestMiddleware)

# First request:

# Response: 200 OK, ETag: W/"abc123"

# Second request with If-None-Match: W/"abc123"

# Response: 304 Not Modified (no body)

```

### Exclude Paths

```python
from fastmiddleware import ETagMiddleware, ETagConfig

config = ETagConfig(
    weak=True,
    exclude_paths={"/api/stream", "/api/events"},
)

app.add_middleware(ETagMiddleware, config=config)

```

## Weak vs Strong ETags

| Type | Format | Use Case |
| ------ | -------- | ---------- |
| Weak | `W/"..."` | Semantically equivalent content |
| Strong | `"..."` | Byte-for-byte identical content |

Use weak ETags when:

- Content may have minor variations (timestamps, whitespace)

- Semantic equality is sufficient

Use strong ETags when:

- Byte-level accuracy is required

- Content must be exactly identical

## Request/Response Flow

```text
Client: GET /api/users
Server: 200 OK
        ETag: W/"abc123"
        Body: [...]

Client: GET /api/users
        If-None-Match: W/"abc123"
Server: 304 Not Modified
        (no body)

Client: GET /api/users
        If-None-Match: W/"abc123"
Server: 200 OK  (content changed)
        ETag: W/"def456"
        Body: [...]

```

## Related Middlewares

- [ConditionalRequestMiddleware](conditional-request.md) - Handle conditional requests
- [CacheMiddleware](cache.md) - HTTP caching headers
- [ResponseCacheMiddleware](response-cache.md) - Server-side caching
