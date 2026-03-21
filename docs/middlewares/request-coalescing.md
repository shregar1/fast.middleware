# RequestCoalescingMiddleware

Coalesce identical concurrent requests into a single execution.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestCoalescingMiddleware

app = FastAPI()

app.add_middleware(
    RequestCoalescingMiddleware,
    window=0.1,  # 100ms window
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `window` | `float` | `0.1` | Coalescing window (seconds) |
| `include_paths` | `set[str]` | `None` | Paths to coalesce (None = all) |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip |

## How It Works

1. Multiple identical requests arrive within the window
2. Only the first request is executed
3. All waiting requests receive the same response
4. Reduces backend load for cache misses

## Examples

### Basic Usage

```python
app.add_middleware(
    RequestCoalescingMiddleware,
    window=0.1,  # 100ms
)

# 10 identical requests in 100ms → 1 backend call, 10 responses

```

### Longer Window

```python
app.add_middleware(
    RequestCoalescingMiddleware,
    window=1.0,  # 1 second
)

```

### Specific Paths

```python
app.add_middleware(
    RequestCoalescingMiddleware,
    window=0.1,
    include_paths={
        "/api/popular",
        "/api/trending",
        "/api/config",
    },
)

```

### Exclude Dynamic Endpoints

```python
app.add_middleware(
    RequestCoalescingMiddleware,
    window=0.1,
    exclude_paths={
        "/api/user/*",  # User-specific
        "/api/cart",    # Session-specific
    },
)

```

### With Caching

```python
from fastmiddleware import RequestCoalescingMiddleware, ResponseCacheMiddleware

# Coalescing first (outer)
app.add_middleware(
    RequestCoalescingMiddleware,
    window=0.1,
)

# Cache second (inner)
app.add_middleware(
    ResponseCacheMiddleware,
    default_ttl=60,
)

```

## Request Identity

Requests are considered identical if:

- Same HTTP method

- Same path

- Same query parameters

- Same body hash (for POST/PUT)

## Performance Benefits

| Scenario | Without Coalescing | With Coalescing |
| ---------- | ------------------- | ----------------- |
| 100 identical requests/100ms | 100 backend calls | 1 backend call |
| Cache miss thundering herd | DB overload | Single query |

## Response Headers

```http
X-Coalesced: true
X-Coalesced-Count: 15

```

## Use Cases

1. **Cache Miss Storms** - Prevent thundering herd
2. **Popular Content** - Handle viral traffic
3. **API Gateways** - Reduce backend load
4. **Rate Limited APIs** - Maximize external API usage

## Related Middlewares

- [RequestDedupMiddleware](request-dedup.md) - Deduplicate requests
- [ResponseCacheMiddleware](response-cache.md) - Response caching
- [LoadSheddingMiddleware](load-shedding.md) - Load shedding
