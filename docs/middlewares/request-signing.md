# RequestSigningMiddleware

Validate HMAC request signatures.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestSigningMiddleware

app = FastAPI()

app.add_middleware(
    RequestSigningMiddleware,
    secret_key="your-shared-secret",
    signature_header="X-Signature",
    algorithm="sha256",
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `secret_key` | `str` | Required | Shared secret key |
| `signature_header` | `str` | `"X-Signature"` | Header containing signature |
| `algorithm` | `str` | `"sha256"` | Hash algorithm |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip validation |

## Signature Format

The signature is computed as:

```text
HMAC-SHA256(secret, "{timestamp}.{method}.{path}.{body}")

```

## Required Client Headers

```http
X-Signature: sha256=a1b2c3d4e5f6...
X-Timestamp: 1705574400

```

## Examples

### Basic Usage

```python
app.add_middleware(
    RequestSigningMiddleware,
    secret_key="my-secret-key",
)

```

### Exclude Public Endpoints

```python
app.add_middleware(
    RequestSigningMiddleware,
    secret_key="my-secret-key",
    exclude_paths={"/health", "/public", "/docs"},
)

```

### Different Algorithm

```python
app.add_middleware(
    RequestSigningMiddleware,
    secret_key="my-secret-key",
    algorithm="sha512",
)

```

### Client Implementation (Python)

```python
import hmac
import hashlib
import time
import requests

def sign_request(method, path, body, secret):
    timestamp = str(int(time.time()))
    message = f"{timestamp}.{method}.{path}.{body}"
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return {
        "X-Timestamp": timestamp,
        "X-Signature": f"sha256={signature}",
    }

# Usage
headers = sign_request("POST", "/api/data", '{"key": "value"}', "secret")
requests.post("http://api/api/data", json={"key": "value"}, headers=headers)

```

### Client Implementation (JavaScript)

```javascript
const crypto = require('crypto');

function signRequest(method, path, body, secret) {
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const message = `${timestamp}.${method}.${path}.${body}`;
    const signature = crypto
        .createHmac('sha256', secret)
        .update(message)
        .digest('hex');

    return {
        'X-Timestamp': timestamp,
        'X-Signature': `sha256=${signature}`,
    };
}

```

### With Replay Prevention

```python
from fastmiddleware import RequestSigningMiddleware, ReplayPreventionMiddleware

# Replay prevention first
app.add_middleware(
    ReplayPreventionMiddleware,
    max_age=300,
)

# Then signature validation
app.add_middleware(
    RequestSigningMiddleware,
    secret_key="my-secret",
)

```

## Error Responses

### Missing Signature

```json
{
    "error": "Bad Request",
    "detail": "Missing required header: X-Signature",
    "status_code": 400
}

```

### Invalid Signature

```json
{
    "error": "Unauthorized",
    "detail": "Invalid signature",
    "status_code": 401
}

```

## Security Best Practices

1. Use a strong, random secret key
2. Rotate keys periodically
3. Use HTTPS in production
4. Combine with replay prevention

## Related Middlewares

- [ReplayPreventionMiddleware](replay-prevention.md) - Prevent replay attacks
- [WebhookMiddleware](webhook.md) - Webhook signatures
- [ResponseSignatureMiddleware](response-signature.md) - Sign responses
