# ResponseTimeMiddleware

Monitor response times against SLAs.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ResponseTimeMiddleware, ResponseTimeSLA

app = FastAPI()

app.add_middleware(
    ResponseTimeMiddleware,
    slas=[
        ResponseTimeSLA("/api/health", target_ms=50, warning_ms=100, critical_ms=200),
        ResponseTimeSLA("/api/search", target_ms=500, warning_ms=1000, critical_ms=2000),
    ],
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `slas` | `list[ResponseTimeSLA]` | `[]` | SLA definitions |
| `default_target_ms` | `float` | `1000` | Default target |
| `log_violations` | `bool` | `True` | Log SLA violations |

## ResponseTimeSLA Fields

| Field | Type | Description |
| ------- | ------ | ------------- |
| `path` | `str` | Path pattern |
| `target_ms` | `float` | Target response time |
| `warning_ms` | `float` | Warning threshold |
| `critical_ms` | `float` | Critical threshold |

## Examples

### Basic SLA Monitoring

```python
app.add_middleware(
    ResponseTimeMiddleware,
    slas=[
        ResponseTimeSLA("/api/health", 50, 100, 200),
        ResponseTimeSLA("/api/users", 200, 500, 1000),
    ],
)

```

### Path Patterns

```python
app.add_middleware(
    ResponseTimeMiddleware,
    slas=[
        ResponseTimeSLA("/api/fast/*", 100, 200, 500),
        ResponseTimeSLA("/api/slow/*", 2000, 5000, 10000),
    ],
)

```

### With Alerting

```python
from fastmiddleware import ResponseTimeMiddleware

class AlertingResponseTime(ResponseTimeMiddleware):
    async def on_sla_violation(self, request, duration_ms, sla):
        if duration_ms > sla.critical_ms:
            await send_alert(
                severity="critical",
                path=request.url.path,
                duration=duration_ms,
                threshold=sla.critical_ms,
            )

app.add_middleware(
    AlertingResponseTime,
    slas=[...],
)

```

### Get Metrics

```python
middleware = ResponseTimeMiddleware(app, slas=[...])

@app.get("/admin/sla-metrics")
async def sla_metrics():
    return {
        "violations": middleware.get_violations(),
        "percentiles": middleware.get_percentiles(),
    }

```

## Response Headers

```http
X-Response-Time-Ms: 145.2
X-SLA-Status: OK

```

or

```http
X-Response-Time-Ms: 2500.5
X-SLA-Status: CRITICAL

```

## Violation Logging

```text
WARNING: SLA violation for /api/search: 1500ms (warning threshold: 1000ms)
CRITICAL: SLA violation for /api/health: 250ms (critical threshold: 200ms)

```

## Metrics

```python
metrics = middleware.get_metrics()

# {

#     "/api/health": {

#         "count": 1000,

#         "p50": 25,

#         "p95": 80,

#         "p99": 150,

#         "violations": 5

#     }

# }

```

## Use Cases

1. **SLA Monitoring** - Track response time commitments
2. **Alerting** - Get notified of slow responses
3. **Debugging** - Identify slow endpoints
4. **Capacity Planning** - Understand performance trends

## Related Middlewares

- [TimingMiddleware](timing.md) - Simple timing header
- [ProfilingMiddleware](profiling.md) - Detailed profiling
- [MetricsMiddleware](metrics.md) - Prometheus metrics
