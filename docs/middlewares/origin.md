# OriginMiddleware

Validate Origin header for cross-origin requests.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import OriginMiddleware

app = FastAPI()

app.add_middleware(
    OriginMiddleware,
    allowed_origins={"https://example.com", "https://app.example.com"},
    block_null_origin=True,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `allowed_origins` | `set[str]` | Required | Allowed origin URLs |
| `block_null_origin` | `bool` | `True` | Block requests with null origin |
| `allow_no_origin` | `bool` | `True` | Allow requests without Origin header |

## Examples

### Basic Origin Validation

```python
app.add_middleware(
    OriginMiddleware,
    allowed_origins={"https://example.com"},
)

# Origin: https://example.com → OK

# Origin: https://evil.com → 403 Forbidden

```

### Multiple Origins

```python
app.add_middleware(
    OriginMiddleware,
    allowed_origins={
        "https://example.com",
        "https://app.example.com",
        "https://staging.example.com",
    },
)

```

### Block Null Origin

```python
app.add_middleware(
    OriginMiddleware,
    allowed_origins={"https://example.com"},
    block_null_origin=True,  # Block sandboxed iframes, file:// URLs
)

```

### Require Origin Header

```python
app.add_middleware(
    OriginMiddleware,
    allowed_origins={"https://example.com"},
    allow_no_origin=False,  # Reject requests without Origin header
)

```

### Development vs Production

```python
import os

origins = {"https://example.com", "https://app.example.com"}

if os.getenv("ENV") == "development":
    origins.add("http://localhost:3000")
    origins.add("http://localhost:8080")

app.add_middleware(
    OriginMiddleware,
    allowed_origins=origins,
)

```

### With CORS

```python
from fastmiddleware import OriginMiddleware, CORSMiddleware

# Origin validation (strict)
app.add_middleware(
    OriginMiddleware,
    allowed_origins={"https://example.com"},
)

# CORS headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
)

```

## Error Response

```json
{
    "error": "Forbidden",
    "detail": "Origin 'https://evil.com' is not allowed",
    "status_code": 403
}

```

## Use Cases

1. **API Security** - Prevent unauthorized cross-origin access
2. **CSRF Protection** - Additional layer with CSRF middleware
3. **Multi-tenant** - Validate tenant-specific origins

## Related Middlewares

- [CORSMiddleware](cors.md) - CORS headers
- [CSRFMiddleware](csrf.md) - CSRF protection
- [TrustedHostMiddleware](trusted-host.md) - Host header validation
