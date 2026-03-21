# TimeoutMiddleware

Request timeout enforcement middleware.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import TimeoutMiddleware, TimeoutConfig

app = FastAPI()

# Basic usage
app.add_middleware(
    TimeoutMiddleware,
    timeout=30.0,  # 30 seconds
)

# With config
config = TimeoutConfig(
    timeout=30.0,
    timeout_response_status=504,
    timeout_message="Request timed out",
    path_timeouts={"/api/upload": 300.0},  # 5 min for uploads
)
app.add_middleware(TimeoutMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `timeout` | `float` | `30.0` | Default timeout in seconds |
| `timeout_response_status` | `int` | `504` | Status code on timeout |
| `timeout_message` | `str` | `"Request timed out"` | Error message |
| `path_timeouts` | `Dict[str, float]` | `{}` | Path-specific timeouts |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## Response Codes

| Code | Description |
| ------ | ------------- |
| 504 | Request timed out (Gateway Timeout) |

## Path-Specific Timeouts

```python
app.add_middleware(
    TimeoutMiddleware,
    timeout=10.0,  # Default 10s
    path_timeouts={
        "/api/upload": 300.0,    # 5 minutes
        "/api/export": 120.0,    # 2 minutes
        "/api/quick": 5.0,       # 5 seconds
    },
)

```

## Notes

- Timeout cancels the request handler via asyncio
- Some operations (like external HTTP calls) may not be cancelled immediately
- Consider using longer timeouts for file uploads/downloads

## Related Middlewares

- [CircuitBreakerMiddleware](circuit-breaker.md)
- [BulkheadMiddleware](bulkhead.md)
