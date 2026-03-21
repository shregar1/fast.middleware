# QuotaMiddleware

Enforce usage quotas per user or API key.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import QuotaMiddleware

app = FastAPI()

app.add_middleware(
    QuotaMiddleware,
    quotas={
        "free": {"requests_per_day": 1000},
        "pro": {"requests_per_day": 100000},
    },
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `quotas` | `dict[str, dict]` | `{}` | Quota definitions by tier |
| `default_tier` | `str` | `"free"` | Default tier for unknown users |
| `tier_header` | `str` | `"X-Tier"` | Header containing user tier |

## Quota Options

| Option | Description |
| -------- | ------------- |
| `requests_per_day` | Daily request limit |
| `requests_per_month` | Monthly request limit |
| `data_per_day` | Daily data transfer (bytes) |
| `data_per_month` | Monthly data transfer (bytes) |

## Examples

### Basic Quota Tiers

```python
app.add_middleware(
    QuotaMiddleware,
    quotas={
        "free": {"requests_per_day": 1000},
        "starter": {"requests_per_day": 10000},
        "pro": {"requests_per_day": 100000},
        "enterprise": {"requests_per_day": 1000000},
    },
)

```

### Multiple Limits

```python
app.add_middleware(
    QuotaMiddleware,
    quotas={
        "free": {
            "requests_per_day": 1000,
            "requests_per_month": 20000,
            "data_per_month": 100 * 1024 * 1024,  # 100 MB
        },
        "pro": {
            "requests_per_day": 50000,
            "requests_per_month": 1000000,
            "data_per_month": 10 * 1024 * 1024 * 1024,  # 10 GB
        },
    },
)

```

### Custom Tier Detection

```python
from fastmiddleware import QuotaMiddleware, QuotaConfig

async def get_user_tier(request) -> str:
    api_key = request.headers.get("X-API-Key")
    if api_key:
        user = await get_user_by_api_key(api_key)
        return user.subscription_tier
    return "free"

config = QuotaConfig(
    quotas={...},
    tier_func=get_user_tier,
)

app.add_middleware(QuotaMiddleware, config=config)

```

### Path-Specific Costs

```python
app.add_middleware(
    QuotaMiddleware,
    quotas={
        "free": {"requests_per_day": 1000},
    },
    path_costs={
        "/api/search": 5,      # Costs 5 requests
        "/api/report": 10,     # Costs 10 requests
        "/api/export": 20,     # Costs 20 requests
    },
)

```

### With Billing Integration

```python
@app.middleware("http")
async def track_quota(request, call_next):
    response = await call_next(request)

    # Get quota usage from request state
    usage = getattr(request.state, "quota_usage", None)
    if usage:
        await billing_service.record_usage(
            user_id=request.state.user_id,
            usage=usage,
        )

    return response

```

## Response Headers

```http
X-Quota-Limit: 1000
X-Quota-Remaining: 750
X-Quota-Reset: 2025-01-19T00:00:00Z

```

## Error Response (Quota Exceeded)

```json
{
    "error": "Quota Exceeded",
    "detail": "You have exceeded your daily quota of 1000 requests",
    "limit": 1000,
    "reset": "2025-01-19T00:00:00Z",
    "status_code": 429
}

```

## Related Middlewares

- [RateLimitMiddleware](rate-limit.md) - Rate limiting
- [CostTrackingMiddleware](cost-tracking.md) - Cost tracking
- [AuthenticationMiddleware](authentication.md) - User authentication
