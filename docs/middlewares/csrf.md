# CSRFMiddleware

Cross-Site Request Forgery protection middleware.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import CSRFMiddleware, CSRFConfig

app = FastAPI()

# Basic usage
app.add_middleware(
    CSRFMiddleware,
    secret_key="your-secret-key-min-32-chars-long",
)

# With configuration
config = CSRFConfig(
    secret_key="your-secret-key",
    cookie_name="csrf_token",
    header_name="X-CSRF-Token",
    cookie_secure=True,
    cookie_httponly=True,
    safe_methods={"GET", "HEAD", "OPTIONS"},
)
app.add_middleware(CSRFMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `secret_key` | `str` | Required | Secret key for token generation |
| `cookie_name` | `str` | `"csrf_token"` | Cookie name for CSRF token |
| `header_name` | `str` | `"X-CSRF-Token"` | Header to check for token |
| `cookie_secure` | `bool` | `True` | Secure flag for cookie |
| `cookie_httponly` | `bool` | `True` | HTTPOnly flag for cookie |
| `safe_methods` | `Set[str]` | `{"GET", "HEAD", "OPTIONS"}` | Methods that don't require CSRF |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude from CSRF |

## How It Works

1. On GET requests, a CSRF token is set in a cookie
2. Client reads the token and includes it in the `X-CSRF-Token` header
3. On POST/PUT/DELETE, the header token must match the cookie token

## Client-Side Usage

```javascript
// Read token from cookie
const csrfToken = document.cookie
  .split('; ')
  .find(row => row.startsWith('csrf_token='))
  ?.split('=')[1];

// Include in requests
fetch('/api/data', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': csrfToken,
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  body: JSON.stringify(data),
});

```

## Response Codes

| Code | Description |
| ------ | ------------- |
| 403 | Missing or invalid CSRF token |

## Related Middlewares

- [SecurityHeadersMiddleware](security-headers.md)
- [CORSMiddleware](cors.md)
