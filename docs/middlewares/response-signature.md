# ResponseSignatureMiddleware

Sign responses for client verification.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ResponseSignatureMiddleware

app = FastAPI()

app.add_middleware(
    ResponseSignatureMiddleware,
    secret_key="your-secret",
    signature_header="X-Response-Signature",
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `secret_key` | `str` | Required | Secret key for signing |
| `signature_header` | `str` | `"X-Response-Signature"` | Header name |
| `algorithm` | `str` | `"sha256"` | Hash algorithm |
| `include_headers` | `list[str]` | `[]` | Headers to include in signature |

## Response Headers

```http
X-Response-Signature: sha256=a1b2c3d4e5f6...
X-Response-Timestamp: 1705574400

```

## Examples

### Basic Usage

```python
app.add_middleware(
    ResponseSignatureMiddleware,
    secret_key="my-secret-key",
)

```

### Include Headers in Signature

```python
app.add_middleware(
    ResponseSignatureMiddleware,
    secret_key="my-secret-key",
    include_headers=["Content-Type", "X-Request-ID"],
)

```

### Client Verification (Python)

```python
import hmac
import hashlib

def verify_response(body, timestamp, signature, secret):
    message = f"{timestamp}.{body}"
    expected = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

# Usage
response = requests.get("http://api/data")
body = response.text
timestamp = response.headers["X-Response-Timestamp"]
signature = response.headers["X-Response-Signature"]

if verify_response(body, timestamp, signature, "my-secret"):
    print("Response is authentic")
else:
    print("Response may be tampered!")

```

### Client Verification (JavaScript)

```javascript
const crypto = require('crypto');

function verifyResponse(body, timestamp, signature, secret) {
    const message = `${timestamp}.${body}`;
    const expected = crypto
        .createHmac('sha256', secret)
        .update(message)
        .digest('hex');

    return `sha256=${expected}` === signature;
}

```

### Exclude Paths

```python
from fastmiddleware import ResponseSignatureMiddleware, ResponseSignatureConfig

config = ResponseSignatureConfig(
    secret_key="my-secret",
    exclude_paths={"/health", "/metrics"},
)

app.add_middleware(ResponseSignatureMiddleware, config=config)

```

## Signature Calculation

```text
HMAC-SHA256(secret, "{timestamp}.{body}")

```

Where:

- `timestamp`: Unix timestamp

- `body`: Response body content

## Use Cases

1. **API Security** - Verify response authenticity
2. **Man-in-the-Middle Prevention** - Detect tampering
3. **Audit Trails** - Prove response integrity
4. **Regulatory Compliance** - Non-repudiation

## Related Middlewares

- [RequestSigningMiddleware](request-signing.md) - Sign requests
- [WebhookMiddleware](webhook.md) - Webhook verification
- [SecurityHeadersMiddleware](security-headers.md) - Security headers
