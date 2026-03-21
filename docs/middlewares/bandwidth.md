# BandwidthMiddleware

Throttle response bandwidth to control download speeds.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import BandwidthMiddleware

app = FastAPI()

app.add_middleware(
    BandwidthMiddleware,
    bytes_per_second=512 * 1024,  # 512 KB/s
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `bytes_per_second` | `int` | `1048576` | Maximum bytes per second (1 MB) |
| `burst_size` | `int` | `None` | Allow burst up to this size |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip throttling |

## Examples

### Basic Bandwidth Limiting

```python
app.add_middleware(
    BandwidthMiddleware,
    bytes_per_second=100 * 1024,  # 100 KB/s
)

```

### With Burst Allowance

```python
app.add_middleware(
    BandwidthMiddleware,
    bytes_per_second=256 * 1024,  # 256 KB/s sustained
    burst_size=1024 * 1024,  # Allow 1 MB burst
)

```

### Exclude Static Files

```python
app.add_middleware(
    BandwidthMiddleware,
    bytes_per_second=512 * 1024,
    exclude_paths={"/static", "/assets"},
)

```

### Per-Tier Bandwidth (with custom logic)

```python
from fastmiddleware import BandwidthMiddleware

class TieredBandwidthMiddleware(BandwidthMiddleware):
    async def get_limit(self, request):
        tier = request.state.user_tier
        limits = {
            "free": 100 * 1024,      # 100 KB/s
            "pro": 1024 * 1024,      # 1 MB/s
            "enterprise": 10 * 1024 * 1024,  # 10 MB/s
        }
        return limits.get(tier, limits["free"])

app.add_middleware(TieredBandwidthMiddleware)

```

## Use Cases

1. **Fair Usage** - Prevent bandwidth abuse
2. **Cost Control** - Limit egress bandwidth costs
3. **QoS** - Ensure consistent experience for all users
4. **Tiered Plans** - Different speeds for different subscription tiers

## Response Headers

```http
X-Bandwidth-Limit: 524288
X-Bandwidth-Remaining: 423000

```

## Related Middlewares

- [RateLimitMiddleware](rate-limit.md) - Request rate limiting
- [QuotaMiddleware](quota.md) - Usage quota enforcement
- [LoadSheddingMiddleware](load-shedding.md) - Shed load under pressure
