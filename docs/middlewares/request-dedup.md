# RequestDedupMiddleware

Deduplicate identical requests within a time window.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestDedupMiddleware

app = FastAPI()

app.add_middleware(
    RequestDedupMiddleware,
    window=1.0,  # 1 second window
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `window` | `float` | `1.0` | Deduplication window (seconds) |
| `methods` | `set[str]` | `{"POST", "PUT"}` | Methods to deduplicate |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip |

## How It Works

1. Client sends a request
2. Request fingerprint is computed
3. If same fingerprint within window, return 429
4. Otherwise, process normally

## Examples

### Basic Deduplication

```python
app.add_middleware(
    RequestDedupMiddleware,
    window=1.0,  # 1 second
)

# Double-click protection for form submissions

```

### Longer Window

```python
app.add_middleware(
    RequestDedupMiddleware,
    window=5.0,  # 5 seconds
)

```

### Include GET Requests

```python
app.add_middleware(
    RequestDedupMiddleware,
    window=1.0,
    methods={"GET", "POST", "PUT", "DELETE"},
)

```

### Exclude Certain Paths

```python
app.add_middleware(
    RequestDedupMiddleware,
    window=1.0,
    exclude_paths={"/api/poll", "/api/events"},
)

```

### With Idempotency Keys

```python
from fastmiddleware import RequestDedupMiddleware, IdempotencyMiddleware

# Dedup first (for accidental duplicates)
app.add_middleware(
    RequestDedupMiddleware,
    window=1.0,
)

# Idempotency second (for intentional retries)
app.add_middleware(
    IdempotencyMiddleware,
    ttl=3600,
)

```

## Request Fingerprint

The fingerprint includes:

- HTTP method

- Path

- Query parameters (sorted)

- Body hash

- Client IP (optional)

## Duplicate Response

```json
{
    "error": "Duplicate Request",
    "detail": "This request was already processed within the last 1.0 seconds",
    "status_code": 429
}

```

With `Retry-After` header.

## Use Cases

1. **Double-Click Prevention** - Form submissions
2. **Mobile Apps** - Retry on poor connection
3. **API Clients** - Buggy retry logic
4. **Webhooks** - Duplicate webhook deliveries

## Difference from Coalescing

| Feature | Dedup | Coalescing |
| --------- | ------- | ------------ |
| Behavior | Reject duplicate | Wait and share |
| Response | 429 error | Same response |
| Use case | Prevent double-submit | Reduce load |

## Related Middlewares

- [RequestCoalescingMiddleware](request-coalescing.md) - Request coalescing
- [IdempotencyMiddleware](idempotency.md) - Idempotency keys
- [RateLimitMiddleware](rate-limit.md) - Rate limiting
