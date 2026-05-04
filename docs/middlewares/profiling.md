# ProfilingMiddleware

Profile request performance for debugging and optimization.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ProfilingMiddleware

app = FastAPI()

app.add_middleware(
    ProfilingMiddleware,
    enabled=True,
    threshold_ms=100,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `enabled` | `bool` | `False` | Enable profiling |
| `threshold_ms` | `float` | `100` | Only profile requests > threshold |
| `include_paths` | `set[str]` | `None` | Paths to profile (None = all) |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip |

## Examples

### Basic Profiling

```python
app.add_middleware(
    ProfilingMiddleware,
    enabled=True,
    threshold_ms=100,  # Only slow requests
)

```

### Profile Specific Paths

```python
app.add_middleware(
    ProfilingMiddleware,
    enabled=True,
    include_paths={"/api/search", "/api/reports"},
    threshold_ms=50,
)

```

### Exclude Health Checks

```python
app.add_middleware(
    ProfilingMiddleware,
    enabled=True,
    exclude_paths={"/health", "/metrics", "/ready"},
)

```

### Development Only

```python
import os

app.add_middleware(
    ProfilingMiddleware,
    enabled=os.getenv("ENV") == "development",
    threshold_ms=0,  # Profile all requests
)

```

### With Custom Handler

```python
async def profile_handler(profile_data: dict):
    if profile_data["duration_ms"] > 1000:
        await alert_slow_request(profile_data)
    await store_profile(profile_data)

app.add_middleware(
    ProfilingMiddleware,
    enabled=True,
    handler=profile_handler,
)

```

## Profile Data

```json
{
    "request_id": "abc-123",
    "path": "/api/users",
    "method": "GET",
    "duration_ms": 245.6,
    "status_code": 200,
    "timestamp": "2025-01-18T10:30:00Z",
    "profile": {
        "total_time": 0.2456,
        "db_time": 0.1823,
        "serialization_time": 0.0234,
        "other": 0.0399
    },
    "memory_mb": 45.2,
    "query_count": 5
}

```

## Response Headers

When profiling is active:

```http
X-Profile-Enabled: true
X-Profile-Duration-Ms: 245.6
X-Profile-Id: abc-123

```

## Accessing Profile Data

```python
@app.get("/admin/profiles")
async def get_profiles():
    profiles = profiling_middleware.get_recent_profiles(100)
    return {"profiles": profiles}

@app.get("/admin/slow-requests")
async def get_slow_requests():
    slow = profiling_middleware.get_slow_requests(threshold_ms=500)
    return {"slow_requests": slow}

```

## Use Cases

1. **Performance Optimization** - Identify slow endpoints
2. **Debugging** - Detailed timing breakdown
3. **Monitoring** - Track performance trends
4. **SLA Compliance** - Verify response times

## Related Middlewares

- [ServerTimingMiddleware](server-timing.md) - Server-Timing header
- [TimingMiddleware](timing.md) - Simple timing header
- [MetricsMiddleware](metrics.md) - Prometheus metrics
