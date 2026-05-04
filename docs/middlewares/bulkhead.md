# BulkheadMiddleware

Bulkhead pattern for resource isolation.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import BulkheadMiddleware, BulkheadConfig

app = FastAPI()

# Basic usage
app.add_middleware(
    BulkheadMiddleware,
    max_concurrent=100,
    max_waiting=50,
)

# With config
config = BulkheadConfig(
    max_concurrent=100,    # Max concurrent requests
    max_waiting=50,        # Max queue size
    timeout=30.0,          # Max wait time
    per_path=False,        # Global or per-path
    path_limits={"/api/heavy": 10},  # Path-specific limits
)
app.add_middleware(BulkheadMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `max_concurrent` | `int` | `100` | Max concurrent requests |
| `max_waiting` | `int` | `50` | Max waiting queue size |
| `timeout` | `float` | `30.0` | Max wait time in seconds |
| `per_path` | `bool` | `False` | Apply limits per-path |
| `path_limits` | `Dict[str, int]` | `{}` | Path-specific limits |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## How It Works

```text
Incoming Request
      │
      ▼
[Within max_concurrent?] ──No──> [Within max_waiting?] ──No──> 503
      │                                   │
      │ Yes                               │ Yes
      ▼                                   ▼
  Process                              Queue
      │                                   │
      ▼                                   │
  Complete ◄──────────────────────────────┘

```

## Response Codes

| Code | Description |
| ------ | ------------- |
| 503 | Service overloaded (queue full or timeout) |

## Response Headers

| Header | Value |
| -------- | ------- |
| `Retry-After` | Suggested retry time in seconds |

## Use Cases

- Prevent resource exhaustion
- Isolate heavy endpoints
- Fair resource allocation

## Related Middlewares

- [CircuitBreakerMiddleware](circuit-breaker.md)
- [RateLimitMiddleware](rate-limit.md)
- [LoadSheddingMiddleware](load-shedding.md)
