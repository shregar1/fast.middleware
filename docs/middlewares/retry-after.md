# RetryAfterMiddleware

Add Retry-After headers for rate-limited responses.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RetryAfterMiddleware

app = FastAPI()

app.add_middleware(
    RetryAfterMiddleware,
    default_retry_after=60,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `default_retry_after` | `int` | `60` | Default retry seconds |
| `status_codes` | `set[int]` | `{429, 503}` | Status codes to add header |

## Response Headers

```http
Retry-After: 60

```

or with date:

```http
Retry-After: Sat, 18 Jan 2025 10:30:00 GMT

```

## Examples

### Basic Usage

```python
app.add_middleware(
    RetryAfterMiddleware,
    default_retry_after=60,
)

# 429 responses include: Retry-After: 60

```

### Custom Status Codes

```python
app.add_middleware(
    RetryAfterMiddleware,
    default_retry_after=30,
    status_codes={429, 503, 504},
)

```

### With Rate Limiting

```python
from fastmiddleware import RateLimitMiddleware, RetryAfterMiddleware

# Retry-After first (outer)
app.add_middleware(
    RetryAfterMiddleware,
    default_retry_after=60,
)

# Rate limiting second (inner)
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=100,
)

```

### Dynamic Retry Time

```python
from fastmiddleware import RetryAfterMiddleware

class DynamicRetryAfter(RetryAfterMiddleware):
    def get_retry_after(self, request, response) -> int:
        # Use rate limit reset time if available
        reset = response.headers.get("X-RateLimit-Reset")
        if reset:
            return int(reset) - int(time.time())

        # Different delays for different paths
        if request.url.path.startswith("/api/expensive"):
            return 120

        return self.default_retry_after

app.add_middleware(DynamicRetryAfter, default_retry_after=60)

```

### Maintenance Mode

```python
from fastapi import Response

@app.get("/")
async def handler(response: Response):
    if maintenance_mode:
        response.status_code = 503
        response.headers["Retry-After"] = "300"  # 5 minutes
        return {"error": "Service under maintenance"}
    return {"ok": True}

```

## Client Handling

```python
import time

response = requests.get("http://api/resource")
if response.status_code == 429:
    retry_after = int(response.headers.get("Retry-After", 60))
    time.sleep(retry_after)
    response = requests.get("http://api/resource")

```

```javascript
if (response.status === 429) {
    const retryAfter = parseInt(response.headers.get('Retry-After')) |
| 60;
    await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
    // Retry request
}

```

## Use Cases

1. **Rate Limiting** - Tell clients when to retry
2. **Maintenance** - Indicate service unavailable duration
3. **Overload** - Backpressure signaling
4. **Polite APIs** - Client-friendly rate limiting

## Related Middlewares

- [RateLimitMiddleware](rate-limit.md) - Rate limiting
- [MaintenanceMiddleware](maintenance.md) - Maintenance mode
- [LoadSheddingMiddleware](load-shedding.md) - Load shedding
