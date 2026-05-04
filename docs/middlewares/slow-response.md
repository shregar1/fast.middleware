# SlowResponseMiddleware

Add artificial delays for testing (development only).

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
import os
from fastapi import FastAPI
from fastmiddleware import SlowResponseMiddleware

app = FastAPI()

app.add_middleware(
    SlowResponseMiddleware,
    enabled=os.getenv("SLOW_MODE") == "true",
    min_delay=1.0,
    max_delay=3.0,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `enabled` | `bool` | `False` | Enable delays |
| `min_delay` | `float` | `0.5` | Minimum delay (seconds) |
| `max_delay` | `float` | `2.0` | Maximum delay (seconds) |
| `paths` | `set[str]` | `None` | Specific paths to slow |

## ⚠️ Warning

**Never enable in production!** This middleware is for testing slow network conditions only.

## Examples

### Basic Usage

```python
app.add_middleware(
    SlowResponseMiddleware,
    enabled=True,
    min_delay=0.5,
    max_delay=2.0,
)

```

### Environment-Based

```python
import os

app.add_middleware(
    SlowResponseMiddleware,
    enabled=os.getenv("ENV") == "development" and os.getenv("SLOW_MODE") == "true",
    min_delay=1.0,
    max_delay=3.0,
)

```

### Slow Specific Paths

```python
app.add_middleware(
    SlowResponseMiddleware,
    enabled=True,
    min_delay=2.0,
    max_delay=5.0,
    paths={"/api/slow", "/api/upload"},
)

```

### Fixed Delay

```python
app.add_middleware(
    SlowResponseMiddleware,
    enabled=True,
    min_delay=1.0,
    max_delay=1.0,  # Same as min = fixed delay
)

```

### Simulate Network Latency

```python

# Simulate typical network latencies
app.add_middleware(
    SlowResponseMiddleware,
    enabled=True,
    min_delay=0.1,   # 100ms
    max_delay=0.5,   # 500ms
)

```

### Simulate Slow Database

```python
app.add_middleware(
    SlowResponseMiddleware,
    enabled=True,
    min_delay=1.0,
    max_delay=10.0,
    paths={"/api/reports", "/api/analytics"},
)

```

## Response Headers

```http
X-Artificial-Delay-Ms: 1523

```

## Use Cases

1. **Frontend Testing** - Test loading states
2. **Timeout Testing** - Test client timeout handling
3. **UX Testing** - Test user experience with slow responses
4. **Load Testing** - Simulate slow dependencies

## Safety Measures

```python

# Automatically disabled in production
class SafeSlowResponse(SlowResponseMiddleware):
    def __init__(self, app, **kwargs):
        import os
        if os.getenv("ENV") == "production":
            kwargs["enabled"] = False
        super().__init__(app, **kwargs)

```

## Related Middlewares

- [ChaosMiddleware](chaos.md) - Chaos engineering
- [TimeoutMiddleware](timeout.md) - Request timeouts
- [ProfilingMiddleware](profiling.md) - Performance profiling
