# XFFTrustMiddleware

Handle X-Forwarded-For headers securely.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import XFFTrustMiddleware

app = FastAPI()

app.add_middleware(
    XFFTrustMiddleware,
    trusted_proxies=["10.0.0.0/8", "172.16.0.0/12"],
    depth=2,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `trusted_proxies` | `list[str]` | `[]` | Trusted proxy IPs/CIDRs |
| `depth` | `int` | `1` | Number of proxies to skip |
| `header_name` | `str` | `"X-Forwarded-For"` | Header name |

## How It Works

X-Forwarded-For contains a chain of IPs:

```http
X-Forwarded-For: client, proxy1, proxy2

```

The middleware:

1. Validates the rightmost IPs are trusted proxies
2. Extracts the real client IP from the chain
3. Sets `request.client.host` to the real IP

## Examples

### Behind One Proxy

```python
app.add_middleware(
    XFFTrustMiddleware,
    trusted_proxies=["10.0.0.1"],
    depth=1,
)

# X-Forwarded-For: 203.0.113.50, 10.0.0.1

# Real IP: 203.0.113.50

```

### Behind Multiple Proxies

```python
app.add_middleware(
    XFFTrustMiddleware,
    trusted_proxies=["10.0.0.0/8"],
    depth=2,
)

# X-Forwarded-For: 203.0.113.50, 10.0.0.1, 10.0.0.2

# Real IP: 203.0.113.50

```

### Cloud Load Balancers

```python

# AWS ALB
app.add_middleware(
    XFFTrustMiddleware,
    trusted_proxies=["10.0.0.0/8", "172.16.0.0/12"],
    depth=1,
)

# GCP Load Balancer
app.add_middleware(
    XFFTrustMiddleware,
    trusted_proxies=["35.191.0.0/16", "130.211.0.0/22"],
    depth=1,
)

# Cloudflare
app.add_middleware(
    XFFTrustMiddleware,
    trusted_proxies=[
        "173.245.48.0/20",
        "103.21.244.0/22",
        "103.22.200.0/22",
        # ... more Cloudflare IPs
    ],
    depth=1,
)

```

### Trust All Private IPs

```python
app.add_middleware(
    XFFTrustMiddleware,
    trusted_proxies=[
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "127.0.0.0/8",
    ],
    depth=3,
)

```

### With Rate Limiting

```python
from fastmiddleware import XFFTrustMiddleware, RateLimitMiddleware

# XFF trust first (sets real IP)
app.add_middleware(
    XFFTrustMiddleware,
    trusted_proxies=["10.0.0.0/8"],
    depth=1,
)

# Rate limiting uses real IP
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=100,
)

```

## Security Warning

⚠️ **Never trust X-Forwarded-For without validation!**

An attacker can spoof the header:

```http
X-Forwarded-For: fake-ip, attacker-ip

```

Only trust the rightmost IPs from known proxies.

## Request State

```python
request.state.original_client_ip  # Original client IP
request.state.xff_chain  # Full XFF chain

```

## Related Middlewares

- [RealIPMiddleware](real-ip.md) - Extract real IP
- [IPFilterMiddleware](ip-filter.md) - IP filtering
- [GeoIPMiddleware](geoip.md) - GeoIP detection
