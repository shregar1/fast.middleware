# LoadSheddingMiddleware

Shed load during high traffic to maintain system stability.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import LoadSheddingMiddleware

app = FastAPI()

app.add_middleware(
    LoadSheddingMiddleware,
    max_concurrent=1000,
    shed_probability=0.5,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `max_concurrent` | `int` | `1000` | Max concurrent requests before shedding |
| `shed_probability` | `float` | `0.5` | Probability of shedding when over limit |
| `priority_paths` | `set[str]` | `set()` | Paths that are never shed |

## How It Works

1. Tracks number of concurrent requests
2. When over `max_concurrent`, randomly sheds requests
3. Shed probability determines how aggressively to reject
4. Priority paths bypass load shedding

## Examples

### Basic Load Shedding

```python
app.add_middleware(
    LoadSheddingMiddleware,
    max_concurrent=500,
    shed_probability=0.3,  # Shed 30% of excess requests
)

```

### Protect Critical Paths

```python
app.add_middleware(
    LoadSheddingMiddleware,
    max_concurrent=1000,
    shed_probability=0.5,
    priority_paths={"/health", "/metrics", "/api/critical"},
)

```

### Aggressive Shedding

```python
app.add_middleware(
    LoadSheddingMiddleware,
    max_concurrent=100,
    shed_probability=0.9,  # Shed 90% when overloaded
)

```

### Gradual Shedding

```python

# Custom implementation for gradual shedding
from fastmiddleware import LoadSheddingMiddleware

class GradualLoadShedding(LoadSheddingMiddleware):
    def get_shed_probability(self, current_load: int) -> float:
        if current_load < self.max_concurrent:
            return 0.0

        # Increase probability as load increases
        overload_ratio = current_load / self.max_concurrent
        return min(0.9, (overload_ratio - 1) * 0.5)

app.add_middleware(GradualLoadShedding, max_concurrent=1000)

```

### With Circuit Breaker

```python
from fastmiddleware import LoadSheddingMiddleware, CircuitBreakerMiddleware

# Load shedding first (outer)
app.add_middleware(
    LoadSheddingMiddleware,
    max_concurrent=1000,
    shed_probability=0.5,
)

# Circuit breaker second (inner)
app.add_middleware(
    CircuitBreakerMiddleware,
    failure_threshold=5,
    recovery_timeout=30,
)

```

## Response on Shed

```json
{
    "error": "Service Overloaded",
    "detail": "Server is currently overloaded. Please retry later.",
    "status_code": 503
}

```

## Response Headers

```http
Retry-After: 5
X-Load-Shed: true

```

## Metrics

```python

# Get current load metrics
@app.get("/admin/load")
async def get_load():
    return {
        "current_concurrent": load_shedding.current_concurrent,
        "max_concurrent": load_shedding.max_concurrent,
        "shed_count": load_shedding.shed_count,
    }

```

## Use Cases

1. **Traffic Spikes** - Handle sudden load increases
2. **DDoS Mitigation** - Reduce impact of attacks
3. **Graceful Degradation** - Maintain responsiveness under load
4. **Cost Control** - Limit resource usage

## Related Middlewares

- [BulkheadMiddleware](bulkhead.md) - Isolation pattern
- [CircuitBreakerMiddleware](circuit-breaker.md) - Circuit breaker pattern
- [RateLimitMiddleware](rate-limit.md) - Rate limiting
