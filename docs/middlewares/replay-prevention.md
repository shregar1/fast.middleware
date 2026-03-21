# ReplayPreventionMiddleware

Prevent replay attacks using timestamps and nonces.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ReplayPreventionMiddleware

app = FastAPI()

app.add_middleware(
    ReplayPreventionMiddleware,
    max_age=300,
    timestamp_header="X-Timestamp",
    nonce_header="X-Nonce",
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `max_age` | `int` | `300` | Max age of request (seconds) |
| `timestamp_header` | `str` | `"X-Timestamp"` | Timestamp header name |
| `nonce_header` | `str` | `"X-Nonce"` | Nonce header name |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip validation |

## How It Works

1. Client includes timestamp and unique nonce in request
2. Server validates timestamp is within `max_age`
3. Server checks nonce hasn't been used before
4. Nonces are stored and expire after `max_age`

## Required Client Headers

```http
X-Timestamp: 1705574400
X-Nonce: a1b2c3d4-e5f6-7890-abcd-ef1234567890

```

## Examples

### Basic Usage

```python
app.add_middleware(
    ReplayPreventionMiddleware,
    max_age=300,  # 5 minutes
)

```

### Exclude Public Endpoints

```python
app.add_middleware(
    ReplayPreventionMiddleware,
    max_age=300,
    exclude_paths={"/health", "/public", "/docs"},
)

```

### Shorter Window for Sensitive Endpoints

```python
app.add_middleware(
    ReplayPreventionMiddleware,
    max_age=60,  # 1 minute
)

```

### Client Implementation (Python)

```python
import time
import uuid
import requests

def make_secure_request(url, data):
    headers = {
        "X-Timestamp": str(int(time.time())),
        "X-Nonce": str(uuid.uuid4()),
    }
    return requests.post(url, json=data, headers=headers)

```

### Client Implementation (JavaScript)

```javascript
async function secureRequest(url, data) {
    const headers = {
        'X-Timestamp': Math.floor(Date.now() / 1000).toString(),
        'X-Nonce': crypto.randomUUID(),
        'Content-Type': 'application/json',
    };

    return fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(data),
    });
}

```

### With Request Signing

```python
from fastmiddleware import ReplayPreventionMiddleware, RequestSigningMiddleware

# Replay prevention first
app.add_middleware(
    ReplayPreventionMiddleware,
    max_age=300,
)

# Then signature validation
app.add_middleware(
    RequestSigningMiddleware,
    secret_key="your-secret",
)

```

## Error Responses

### Expired Timestamp

```json
{
    "error": "Request Expired",
    "detail": "Timestamp is older than 300 seconds",
    "status_code": 401
}

```

### Replay Detected

```json
{
    "error": "Replay Detected",
    "detail": "Nonce has already been used",
    "status_code": 401
}

```

### Missing Headers

```json
{
    "error": "Bad Request",
    "detail": "Missing required header: X-Timestamp",
    "status_code": 400
}

```

## Related Middlewares

- [RequestSigningMiddleware](request-signing.md) - HMAC signatures
- [WebhookMiddleware](webhook.md) - Webhook verification
- [CSRFMiddleware](csrf.md) - CSRF protection
