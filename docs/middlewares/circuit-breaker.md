# CircuitBreakerMiddleware

Circuit breaker pattern implementation for resilience.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import CircuitBreakerMiddleware, CircuitBreakerConfig, CircuitState

app = FastAPI()

# Basic usage
app.add_middleware(
    CircuitBreakerMiddleware,
    failure_threshold=5,
    recovery_timeout=30,
)

# With config
config = CircuitBreakerConfig(
    failure_threshold=5,      # Failures before opening
    recovery_timeout=30,      # Seconds before trying again
    half_open_requests=3,     # Requests in half-open state
    failure_status_codes={500, 502, 503, 504},
)
app.add_middleware(CircuitBreakerMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `failure_threshold` | `int` | `5` | Failures before circuit opens |
| `recovery_timeout` | `int` | `30` | Seconds before testing recovery |
| `half_open_requests` | `int` | `3` | Test requests in half-open |
| `failure_status_codes` | `Set[int]` | `{500, 502, 503, 504}` | Status codes that count as failures |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## Circuit States

| State | Description |
| ------- | ------------- |
| `CLOSED` | Normal operation, requests pass through |
| `OPEN` | Circuit is open, requests immediately fail |
| `HALF_OPEN` | Testing if service recovered |

## State Transitions

```text
CLOSED --[failure_threshold reached]--> OPEN
OPEN --[recovery_timeout elapsed]--> HALF_OPEN
HALF_OPEN --[request succeeds]--> CLOSED
HALF_OPEN --[request fails]--> OPEN

```

## Response Codes

| Code | Description |
| ------ | ------------- |
| 503 | Circuit is open, service unavailable |

## Response Headers

| Header | Value |
| -------- | ------- |
| `X-Circuit-State` | Current circuit state |
| `Retry-After` | Seconds until retry (when open) |

## Related Middlewares

- [BulkheadMiddleware](bulkhead.md) - Isolation pattern
- [LoadSheddingMiddleware](load-shedding.md) - Load management
