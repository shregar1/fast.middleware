# RequestFingerprintMiddleware

Generate unique fingerprints for requests.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestFingerprintMiddleware, get_fingerprint

app = FastAPI()

app.add_middleware(RequestFingerprintMiddleware)

@app.get("/")
async def handler():
    return {"fingerprint": get_fingerprint()}

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `include_ip` | `bool` | `True` | Include client IP |
| `include_user_agent` | `bool` | `True` | Include User-Agent |
| `include_headers` | `list[str]` | `[]` | Additional headers |
| `hash_algorithm` | `str` | `"sha256"` | Hash algorithm |

## Helper Functions

### `get_fingerprint() -> str`

Returns the fingerprint for the current request.

```python
from fastmiddleware import get_fingerprint

@app.get("/track")
async def track():
    fp = get_fingerprint()
    await analytics.record(fp)
    return {"tracked": True}

```

## Examples

### Basic Fingerprinting

```python
app.add_middleware(RequestFingerprintMiddleware)

# Fingerprint: sha256 hash of IP + User-Agent

```

### Include Accept-Language

```python
app.add_middleware(
    RequestFingerprintMiddleware,
    include_headers=["Accept-Language", "Accept-Encoding"],
)

```

### Exclude IP (Privacy)

```python
app.add_middleware(
    RequestFingerprintMiddleware,
    include_ip=False,
)

```

### Custom Components

```python
app.add_middleware(
    RequestFingerprintMiddleware,
    include_ip=True,
    include_user_agent=True,
    include_headers=[
        "Accept-Language",
        "Accept-Encoding",
        "Sec-CH-UA",
        "Sec-CH-UA-Platform",
    ],
)

```

### Device Tracking

```python
from fastmiddleware import RequestFingerprintMiddleware, get_fingerprint

app.add_middleware(RequestFingerprintMiddleware)

@app.get("/session")
async def session(request: Request):
    fp = get_fingerprint()

    # Check if we've seen this device
    device = await db.get_device(fp)
    if not device:
        device = await db.create_device(fp)

    return {"device_id": device.id}

```

### Fraud Detection

```python
@app.post("/purchase")
async def purchase(data: PurchaseData):
    fp = get_fingerprint()

    # Check for suspicious patterns
    recent_purchases = await db.get_purchases_by_fingerprint(fp, hours=24)
    if len(recent_purchases) > 10:
        raise HTTPException(429, "Too many purchases from this device")

    return await process_purchase(data)

```

### Rate Limiting by Fingerprint

```python
from fastmiddleware import RateLimitMiddleware, get_fingerprint

# Custom key function using fingerprint
def fingerprint_key(request):
    return get_fingerprint()

app.add_middleware(RequestFingerprintMiddleware)
app.add_middleware(
    RateLimitMiddleware,
    key_func=fingerprint_key,
    requests_per_minute=60,
)

```

## Fingerprint Components

| Component | Example |
| ----------- | --------- |
| IP Address | `192.168.1.100` |
| User-Agent | `Mozilla/5.0...` |
| Accept-Language | `en-US,en;q=0.9` |
| Accept-Encoding | `gzip, deflate, br` |
| Custom headers | As specified |

## Request State

```python
request.state.fingerprint  # The computed fingerprint

```

## Privacy Considerations

- Consider GDPR implications
- Offer opt-out for users
- Don't use for authentication alone

## Related Middlewares

- [UserAgentMiddleware](user-agent.md) - Parse User-Agent
- [RealIPMiddleware](real-ip.md) - Get real IP
- [ClientHintsMiddleware](client-hints.md) - Client hints
