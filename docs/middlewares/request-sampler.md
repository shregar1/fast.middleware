# RequestSamplerMiddleware

Sample requests for analytics and logging.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestSamplerMiddleware, is_sampled

app = FastAPI()

app.add_middleware(
    RequestSamplerMiddleware,
    rate=0.1,  # 10% sampling
)

@app.get("/")
async def handler():
    if is_sampled():
        log_detailed_metrics()
    return {"sampled": is_sampled()}

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `rate` | `float` | `0.1` | Sampling rate (0.0 - 1.0) |
| `path_rates` | `dict[str, float]` | `{}` | Per-path sampling rates |
| `always_sample` | `set[str]` | `set()` | Paths to always sample |

## Helper Functions

### `is_sampled() -> bool`

Returns True if the current request is sampled.

```python
from fastmiddleware import is_sampled

@app.get("/")
async def handler():
    if is_sampled():
        # Expensive logging/tracing
        await detailed_log()
    return {"ok": True}

```

## Examples

### Basic 10% Sampling

```python
app.add_middleware(
    RequestSamplerMiddleware,
    rate=0.1,  # 10%
)

```

### Per-Path Rates

```python
app.add_middleware(
    RequestSamplerMiddleware,
    rate=0.1,  # Default 10%
    path_rates={
        "/api/high-traffic": 0.01,   # 1% for high traffic
        "/api/critical": 1.0,         # 100% for critical
        "/api/debug": 0.5,            # 50% for debugging
    },
)

```

### Always Sample Certain Paths

```python
app.add_middleware(
    RequestSamplerMiddleware,
    rate=0.1,
    always_sample={"/api/errors", "/api/critical"},
)

```

### Conditional Detailed Logging

```python
from fastmiddleware import is_sampled

@app.get("/search")
async def search(q: str):
    result = await perform_search(q)

    if is_sampled():
        # Only log details for sampled requests
        await log_search_details({
            "query": q,
            "results_count": len(result),
            "response_time": ...,
            "cache_hit": ...,
        })

    return result

```

### Distributed Tracing

```python
from fastmiddleware import RequestSamplerMiddleware, is_sampled
from opentelemetry import trace

app.add_middleware(
    RequestSamplerMiddleware,
    rate=0.01,  # 1% tracing
)

@app.get("/")
async def handler():
    if is_sampled():
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("detailed_span"):
            # Detailed tracing
            ...
    return {"ok": True}

```

### Analytics Sampling

```python
from fastmiddleware import is_sampled

@app.middleware("http")
async def analytics(request, call_next):
    response = await call_next(request)

    if is_sampled():
        await send_to_analytics({
            "path": request.url.path,
            "method": request.method,
            "status": response.status_code,
            "user_agent": request.headers.get("user-agent"),
        })

    return response

```

## Request State

```python
request.state.sampled  # bool - Is this request sampled?

```

## Response Headers

```http
X-Sampled: true

```

## Use Cases

1. **Cost Reduction** - Reduce logging/analytics costs
2. **Performance** - Skip expensive operations
3. **Distributed Tracing** - Sample-based tracing
4. **A/B Testing** - Random user selection

## Related Middlewares

- [ProfilingMiddleware](profiling.md) - Request profiling
- [MetricsMiddleware](metrics.md) - Prometheus metrics
- [AuditMiddleware](audit.md) - Audit logging
