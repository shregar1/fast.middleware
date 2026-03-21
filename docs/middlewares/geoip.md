# GeoIPMiddleware

Extract GeoIP data from CDN headers.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import GeoIPMiddleware, get_geo_data

app = FastAPI()

app.add_middleware(GeoIPMiddleware)

@app.get("/")
async def handler():
    geo = get_geo_data()
    return {
        "country": geo.get("country"),
        "city": geo.get("city"),
    }

```

## How It Works

This middleware extracts GeoIP information from headers set by CDNs and load balancers:

- Cloudflare: `CF-IPCountry`, `CF-IPCity`

- AWS CloudFront: `CloudFront-Viewer-Country`

- Fastly: `Fastly-Geo-Country`

- Akamai: `X-Akamai-Edgescape`

## Helper Functions

### `get_geo_data() -> dict`

Returns GeoIP data for the current request.

```python
from fastmiddleware import get_geo_data

geo = get_geo_data()

# {

#     "country": "US",

#     "country_name": "United States",

#     "city": "San Francisco",

#     "region": "CA",

#     "latitude": 37.7749,

#     "longitude": -122.4194,

#     "timezone": "America/Los_Angeles",

# }

```

## Examples

### Basic GeoIP Detection

```python
app.add_middleware(GeoIPMiddleware)

@app.get("/localize")
async def localize():
    geo = get_geo_data()
    country = geo.get("country", "US")

    currencies = {"US": "USD", "GB": "GBP", "EU": "EUR"}
    return {"currency": currencies.get(country, "USD")}

```

### Country-Based Routing

```python
@app.get("/content")
async def content():
    geo = get_geo_data()
    country = geo.get("country")

    if country in ["CN", "RU"]:
        return RedirectResponse("/regional-content")

    return {"content": "Global content"}

```

### Geo-Based Rate Limiting

```python
from fastmiddleware import GeoIPMiddleware, get_geo_data

@app.middleware("http")
async def geo_rate_limit(request, call_next):
    geo = get_geo_data()
    country = geo.get("country")

    # Higher limits for certain countries
    if country in ["US", "GB", "DE"]:
        request.state.rate_limit = 1000
    else:
        request.state.rate_limit = 100

    return await call_next(request)

```

### GDPR Compliance

```python
@app.get("/api/data")
async def get_data():
    geo = get_geo_data()

    eu_countries = ["DE", "FR", "IT", "ES", "NL", "BE", "AT", "PL", ...]

    if geo.get("country") in eu_countries:
        return {"data": scrub_pii(data), "gdpr": True}

    return {"data": data, "gdpr": False}

```

### Timezone Detection

```python
@app.get("/time")
async def get_time():
    geo = get_geo_data()
    timezone = geo.get("timezone", "UTC")

    from datetime import datetime
    import pytz

    tz = pytz.timezone(timezone)
    local_time = datetime.now(tz)

    return {"local_time": local_time.isoformat(), "timezone": timezone}

```

## Supported CDN Headers

| CDN | Headers |
| ----- | --------- |
| Cloudflare | `CF-IPCountry`, `CF-IPCity`, `CF-IPLatitude`, `CF-IPLongitude` |
| AWS CloudFront | `CloudFront-Viewer-Country`, `CloudFront-Viewer-City` |
| Fastly | `Fastly-Geo-*` |
| Akamai | `X-Akamai-Edgescape` |
| Generic | `X-Geo-Country`, `X-Geo-City` |

## Request State

```python
request.state.geo_data  # Full geo data dictionary

```

## Related Middlewares

- [RealIPMiddleware](real-ip.md) - Extract real client IP
- [LocaleMiddleware](locale.md) - Locale detection
- [IPFilterMiddleware](ip-filter.md) - IP filtering
