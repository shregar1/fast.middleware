# RedirectMiddleware

URL redirects with permanent and temporary options.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RedirectMiddleware, RedirectRule

app = FastAPI()

app.add_middleware(
    RedirectMiddleware,
    rules=[
        RedirectRule("/old-path", "/new-path", permanent=True),
        RedirectRule("/legacy/*", "/api/v2/{path}"),
    ],
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `rules` | `list[RedirectRule]` | `[]` | Redirect rules |

## RedirectRule Fields

| Field | Type | Default | Description |
| ------- | ------ | --------- | ------------- |
| `source` | `str` | Required | Source path pattern |
| `destination` | `str` | Required | Destination path |
| `permanent` | `bool` | `False` | 301 (permanent) vs 307 (temporary) |
| `preserve_query` | `bool` | `True` | Keep query parameters |

## Examples

### Permanent Redirect

```python
app.add_middleware(
    RedirectMiddleware,
    rules=[
        RedirectRule("/blog", "/articles", permanent=True),
    ],
)

# GET /blog → 301 Redirect to /articles

```

### Temporary Redirect

```python
app.add_middleware(
    RedirectMiddleware,
    rules=[
        RedirectRule("/maintenance", "/status", permanent=False),
    ],
)

# GET /maintenance → 307 Redirect to /status

```

### Wildcard Patterns

```python
app.add_middleware(
    RedirectMiddleware,
    rules=[
        RedirectRule("/old-api/*", "/api/v2/{path}"),
    ],
)

# /old-api/users → /api/v2/users

# /old-api/orders/123 → /api/v2/orders/123

```

### Multiple Redirects

```python
app.add_middleware(
    RedirectMiddleware,
    rules=[
        RedirectRule("/home", "/", permanent=True),
        RedirectRule("/about-us", "/about", permanent=True),
        RedirectRule("/contact-us", "/contact", permanent=True),
        RedirectRule("/products", "/shop", permanent=True),
    ],
)

```

### Domain Migration

```python
app.add_middleware(
    RedirectMiddleware,
    rules=[
        RedirectRule("/v1/*", "/v2/{path}", permanent=True),
    ],
)

```

### Preserve Query Parameters

```python
app.add_middleware(
    RedirectMiddleware,
    rules=[
        RedirectRule("/search", "/api/search", preserve_query=True),
    ],
)

# /search?q=hello → /api/search?q=hello

```

### SEO Redirects

```python
app.add_middleware(
    RedirectMiddleware,
    rules=[
        # Canonical URLs
        RedirectRule("/Home", "/", permanent=True),
        RedirectRule("/HOME", "/", permanent=True),

        # Old slugs
        RedirectRule("/old-post-slug", "/new-post-slug", permanent=True),
    ],
)

```

## Status Codes

| Permanent | Status | Use Case |
| ----------- | -------- | ---------- |
| `True` | 301 | Permanent moves, SEO |
| `False` | 307 | Temporary moves, A/B tests |

## Related Middlewares

- [PathRewriteMiddleware](path-rewrite.md) - Internal path rewriting
- [TrailingSlashMiddleware](trailing-slash.md) - Trailing slash handling
- [HTTPSRedirectMiddleware](https-redirect.md) - HTTPS redirects
