# PathRewriteMiddleware

Rewrite request paths without redirecting.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import PathRewriteMiddleware, RewriteRule

app = FastAPI()

app.add_middleware(
    PathRewriteMiddleware,
    rules=[
        RewriteRule("/old-api", "/api/v1"),
        RewriteRule(r"/users/(\d+)", r"/api/users/\1", is_regex=True),
    ],
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `rules` | `list[RewriteRule]` | `[]` | Rewrite rules |

## RewriteRule Fields

| Field | Type | Description |
| ------- | ------ | ------------- |
| `pattern` | `str` | Path pattern to match |
| `replacement` | `str` | Replacement path |
| `is_regex` | `bool` | Treat pattern as regex |

## Examples

### Simple Prefix Rewrite

```python
app.add_middleware(
    PathRewriteMiddleware,
    rules=[
        RewriteRule("/old-api", "/api/v2"),
    ],
)

# /old-api/users → /api/v2/users

```

### Regex Patterns

```python
app.add_middleware(
    PathRewriteMiddleware,
    rules=[
        RewriteRule(
            r"/users/(\d+)/profile",
            r"/api/v2/profiles/\1",
            is_regex=True,
        ),
    ],
)

# /users/123/profile → /api/v2/profiles/123

```

### API Version Rewriting

```python
app.add_middleware(
    PathRewriteMiddleware,
    rules=[
        RewriteRule("/v1/", "/api/v1/"),
        RewriteRule("/v2/", "/api/v2/"),
    ],
)

# /v1/users → /api/v1/users

# /v2/users → /api/v2/users

```

### Legacy URL Support

```python
app.add_middleware(
    PathRewriteMiddleware,
    rules=[
        RewriteRule("/blog", "/articles"),
        RewriteRule("/posts", "/articles"),
        RewriteRule("/feed", "/api/rss"),
    ],
)

```

### Complex Rewrites

```python
app.add_middleware(
    PathRewriteMiddleware,
    rules=[
        # Username to ID
        RewriteRule(
            r"/@([a-zA-Z0-9_]+)",
            r"/api/users/by-username/\1",
            is_regex=True,
        ),
        # Date-based URLs
        RewriteRule(
            r"/archive/(\d{4})/(\d{2})",
            r"/api/posts?year=\1&month=\2",
            is_regex=True,
        ),
    ],
)

# /@johndoe → /api/users/by-username/johndoe

# /archive/2024/01 → /api/posts?year=2024&month=01

```

### Microservice Routing

```python
app.add_middleware(
    PathRewriteMiddleware,
    rules=[
        RewriteRule("/auth/", "/api/auth-service/"),
        RewriteRule("/payments/", "/api/payment-service/"),
        RewriteRule("/notifications/", "/api/notification-service/"),
    ],
)

```

## Difference from Redirect

| Feature | PathRewrite | Redirect |
| --------- | ------------- | ---------- |
| URL in browser | Unchanged | Changes |
| HTTP round-trip | Single | Double |
| Use case | Internal routing | SEO, permanent moves |

## Related Middlewares

- [RedirectMiddleware](redirect.md) - URL redirects
- [ProxyMiddleware](proxy.md) - Reverse proxy
- [TrailingSlashMiddleware](trailing-slash.md) - Trailing slash handling
