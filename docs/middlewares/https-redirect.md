# HTTPSRedirectMiddleware

Redirects HTTP requests to HTTPS.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import HTTPSRedirectMiddleware, HTTPSRedirectConfig

app = FastAPI()

# Basic usage
app.add_middleware(HTTPSRedirectMiddleware)

# With options
app.add_middleware(
    HTTPSRedirectMiddleware,
    permanent=True,  # 301 redirect
    exclude_paths={"/health", "/ready"},
)

# With config
config = HTTPSRedirectConfig(
    permanent=True,
    exclude_paths={"/health"},
    exclude_hosts={"localhost", "127.0.0.1"},
)
app.add_middleware(HTTPSRedirectMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `permanent` | `bool` | `True` | Use 301 (True) or 307 (False) |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude from redirect |
| `exclude_hosts` | `Set[str]` | `{"localhost", "127.0.0.1"}` | Hosts to exclude |

## Response Codes

| Code | Description |
| ------ | ------------- |
| 301 | Permanent redirect (if `permanent=True`) |
| 307 | Temporary redirect (if `permanent=False`) |

## Notes

- The middleware checks `X-Forwarded-Proto` header to detect HTTPS behind proxies
- Exclude localhost by default for development

## Related Middlewares

- [SecurityHeadersMiddleware](security-headers.md) - Adds HSTS header
