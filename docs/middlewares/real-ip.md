# RealIPMiddleware

Extract real client IP from proxy headers.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import RealIPMiddleware, RealIPConfig, get_real_ip

app = FastAPI()

# Basic usage
app.add_middleware(RealIPMiddleware)

# Custom header priority
app.add_middleware(
    RealIPMiddleware,
    headers=[
        "CF-Connecting-IP",    # Cloudflare
        "X-Real-IP",           # nginx
        "True-Client-IP",      # Akamai
        "X-Forwarded-For",     # Standard
    ],
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `headers` | `List[str]` | See below | Headers to check (in order) |
| `trusted_proxies` | `Set[str]` | `set()` | Trusted proxy IPs |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

### Default Header Order

1. `CF-Connecting-IP` (Cloudflare)
2. `X-Real-IP` (nginx)
3. `True-Client-IP` (Akamai)
4. `X-Forwarded-For` (Standard)

## Getting Real IP

```python
from fastmiddleware import get_real_ip

@app.get("/")
async def handler():
    ip = get_real_ip()
    return {"your_ip": ip}

# Or from request state
@app.get("/info")
async def info(request: Request):
    ip = request.state.real_ip
    return {"ip": ip}

```

## CDN/Proxy Headers

| Provider | Header |
| ---------- | -------- |
| Cloudflare | `CF-Connecting-IP` |
| AWS CloudFront | `CloudFront-Viewer-Address` |
| Akamai | `True-Client-IP` |
| nginx | `X-Real-IP` |
| Standard | `X-Forwarded-For` |

## X-Forwarded-For Handling

X-Forwarded-For can contain multiple IPs:

```http
X-Forwarded-For: client, proxy1, proxy2

```

The middleware returns the leftmost (client) IP.

## Security Considerations

⚠️ Only trust these headers if:

1. Your app is behind a known proxy/CDN

2. The proxy/CDN sets these headers

3. Direct access to your app is blocked

## Use Cases

- Rate limiting by real IP
- Geo-location
- Audit logging
- Access control

## Related Middlewares

- [XFFTrustMiddleware](xff-trust.md) - Trusted proxy configuration
- [IPFilterMiddleware](ip-filter.md) - IP-based access control
- [GeoIPMiddleware](geoip.md) - Geographic information
