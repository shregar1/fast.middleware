# CostTrackingMiddleware

Track request costs for billing, quotas, and resource management.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import CostTrackingMiddleware, add_cost, get_request_cost

app = FastAPI()

app.add_middleware(
    CostTrackingMiddleware,
    path_costs={"/api/expensive": 10.0, "/api/cheap": 0.5},
    default_cost=1.0,
)

@app.get("/api/custom")
async def handler():
    add_cost(5.0)  # External API call cost
    return {"total_cost": get_request_cost()}

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `default_cost` | `float` | `1.0` | Default cost per request |
| `path_costs` | `dict[str, float]` | `{}` | Cost overrides by path |
| `method_costs` | `dict[str, float]` | `{}` | Cost multipliers by method |

## Helper Functions

### `get_request_cost() -> float`

Returns the current accumulated cost for the request.

```python
from fastmiddleware import get_request_cost

@app.get("/summary")
async def summary():
    # ... do work ...
    return {"cost": get_request_cost()}

```

### `add_cost(amount: float) -> None`

Add to the request's cost (e.g., for external API calls).

```python
from fastmiddleware import add_cost

@app.get("/ai-analysis")
async def ai_analysis():
    result = await call_openai_api()  # Expensive operation
    add_cost(0.05)  # Add API cost

    images = await generate_images()
    add_cost(0.10)  # Add image generation cost

    return result

```

## Examples

### Basic Path-Based Costs

```python
app.add_middleware(
    CostTrackingMiddleware,
    path_costs={
        "/api/search": 2.0,      # Search is expensive
        "/api/report": 5.0,      # Reports are very expensive
        "/api/health": 0.0,      # Health checks are free
    },
    default_cost=1.0,
)

```

### Method-Based Costs

```python
app.add_middleware(
    CostTrackingMiddleware,
    default_cost=1.0,
    method_costs={
        "GET": 1.0,
        "POST": 2.0,
        "PUT": 2.0,
        "DELETE": 1.5,
    },
)

```

### Track and Report Costs

```python
from fastmiddleware import CostTrackingMiddleware, get_request_cost

app.add_middleware(CostTrackingMiddleware, default_cost=1.0)

@app.middleware("http")
async def log_cost(request, call_next):
    response = await call_next(request)

    cost = get_request_cost()
    user_id = request.state.user_id

    # Log or store for billing
    await billing_service.record_usage(user_id, cost)

    # Add cost to response header
    response.headers["X-Request-Cost"] = str(cost)

    return response

```

### Quota Integration

```python
from fastmiddleware import CostTrackingMiddleware, get_request_cost, add_cost

app.add_middleware(CostTrackingMiddleware)

@app.middleware("http")
async def check_quota(request, call_next):
    user = request.state.user

    # Check if user has enough quota
    estimated_cost = estimate_cost(request)
    if user.remaining_quota < estimated_cost:
        return JSONResponse(
            status_code=429,
            content={"error": "Quota exceeded"}
        )

    response = await call_next(request)

    # Deduct actual cost
    actual_cost = get_request_cost()
    await deduct_quota(user, actual_cost)

    return response

```

## Response Headers

```http
X-Request-Cost: 15.5
X-Cost-Breakdown: base=1.0,api=5.0,storage=9.5

```

## Related Middlewares

- [QuotaMiddleware](quota.md) - Usage quota enforcement
- [RateLimitMiddleware](rate-limit.md) - Request rate limiting
- [MetricsMiddleware](metrics.md) - Request metrics
