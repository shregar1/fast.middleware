# TrailingSlashMiddleware

Handle trailing slashes in URLs.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import TrailingSlashMiddleware, SlashAction

app = FastAPI()

app.add_middleware(
    TrailingSlashMiddleware,
    action=SlashAction.STRIP,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `action` | `SlashAction` | `STRIP` | How to handle trailing slashes |
| `exclude_paths` | `set[str]` | `set()` | Paths to skip |

## SlashAction Options

| Action | Description |
| -------- | ------------- |
| `STRIP` | Remove trailing slash |
| `ADD` | Add trailing slash |
| `REDIRECT` | Redirect to canonical URL |

## Examples

### Strip Trailing Slashes

```python
app.add_middleware(
    TrailingSlashMiddleware,
    action=SlashAction.STRIP,
)

# /api/users/ → /api/users

```

### Add Trailing Slashes

```python
app.add_middleware(
    TrailingSlashMiddleware,
    action=SlashAction.ADD,
)

# /api/users → /api/users/

```

### Redirect to Canonical

```python
app.add_middleware(
    TrailingSlashMiddleware,
    action=SlashAction.REDIRECT,
)

# /api/users/ → 301 Redirect to /api/users

```

### Exclude Certain Paths

```python
app.add_middleware(
    TrailingSlashMiddleware,
    action=SlashAction.STRIP,
    exclude_paths={"/api/static/", "/api/downloads/"},
)

```

### With Redirect Middleware

```python
from fastmiddleware import TrailingSlashMiddleware, RedirectMiddleware

# Handle trailing slash first
app.add_middleware(
    TrailingSlashMiddleware,
    action=SlashAction.STRIP,
)

# Other redirects second
app.add_middleware(
    RedirectMiddleware,
    rules=[...],
)

```

## Behavior by Action

### STRIP

```text
/api/users/ → /api/users (internally rewritten)
/api/users  → /api/users (unchanged)

```

### ADD

```text
/api/users  → /api/users/ (internally rewritten)
/api/users/ → /api/users/ (unchanged)

```

### REDIRECT

```text
/api/users/ → 301 Redirect to /api/users
/api/users  → Normal response

```

## SEO Considerations

- Use `REDIRECT` for SEO to avoid duplicate content
- Choose one style (with or without slash) and stick to it
- 301 redirects pass link equity

## Use Cases

1. **SEO** - Canonical URLs for search engines
2. **Consistency** - Uniform API paths
3. **Compatibility** - Work with different client behaviors

## Related Middlewares

- [RedirectMiddleware](redirect.md) - URL redirects
- [PathRewriteMiddleware](path-rewrite.md) - Path rewriting
- [HTTPSRedirectMiddleware](https-redirect.md) - HTTPS redirects
