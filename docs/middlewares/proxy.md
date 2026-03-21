# ProxyMiddleware

Reverse proxy middleware for routing requests to other services.

## Prerequisites

🌐 Requires httpx: `pip install fast-middleware[proxy]`

## Installation

```bash
pip install fast-middleware[proxy]

# or
pip install fast-middleware[all]

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import ProxyMiddleware, ProxyConfig, ProxyRoute

app = FastAPI()

# Basic usage
app.add_middleware(
    ProxyMiddleware,
    routes=[
        ProxyRoute(
            path_prefix="/api/v2",
            target="http://new-api:8000",
            strip_prefix=True,
        ),
        ProxyRoute(
            path_prefix="/legacy",
            target="http://old-service:3000",
            strip_prefix=False,
        ),
    ],
)

```

## Configuration

### ProxyRoute Options

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `path_prefix` | `str` | Required | URL prefix to match |
| `target` | `str` | Required | Target server URL |
| `strip_prefix` | `bool` | `True` | Remove prefix from forwarded URL |
| `preserve_host` | `bool` | `False` | Keep original Host header |
| `add_headers` | `Dict[str, str]` | `{}` | Headers to add to request |

### Middleware Options

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `routes` | `List[ProxyRoute]` | `[]` | Proxy route definitions |
| `timeout` | `float` | `30.0` | Request timeout |
| `follow_redirects` | `bool` | `False` | Follow HTTP redirects |

## Examples

### Strip Prefix

```python

# Request: /api/v2/users

# Forwarded to: http://new-api:8000/users
ProxyRoute("/api/v2", "http://new-api:8000", strip_prefix=True)

```

### Keep Prefix

```python

# Request: /legacy/data

# Forwarded to: http://old-service:3000/legacy/data
ProxyRoute("/legacy", "http://old-service:3000", strip_prefix=False)

```

### Add Authentication

```python
ProxyRoute(
    path_prefix="/internal",
    target="http://internal-service:8080",
    add_headers={"X-Internal-Auth": "secret-token"},
)

```

## Headers Forwarded

The middleware automatically forwards:

- `X-Forwarded-For`: Client IP chain

- `X-Forwarded-Proto`: Original protocol (http/https)

- `X-Forwarded-Host`: Original host (if preserve_host=True)

## Response Codes

| Code | Description |
| ------ | ------------- |
| 502 | Bad Gateway (target unreachable) |
| 504 | Gateway Timeout |

## Related Middlewares

- [PathRewriteMiddleware](path-rewrite.md) - URL rewriting
- [RedirectMiddleware](redirect.md) - HTTP redirects
