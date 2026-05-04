# RouteAuthMiddleware

Per-route authentication requirements.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RouteAuthMiddleware, RouteAuth

app = FastAPI()

app.add_middleware(
    RouteAuthMiddleware,
    routes=[
        RouteAuth("/api/public", require_auth=False),
        RouteAuth("/api/user", require_auth=True),
        RouteAuth("/api/admin", require_auth=True, required_roles=["admin"]),
    ],
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `routes` | `list[RouteAuth]` | `[]` | Route auth rules |
| `default_require_auth` | `bool` | `True` | Default auth requirement |

## RouteAuth Fields

| Field | Type | Description |
| ------- | ------ | ------------- |
| `path` | `str` | Path pattern |
| `require_auth` | `bool` | Require authentication |
| `required_roles` | `list[str]` | Required roles |
| `required_scopes` | `list[str]` | Required OAuth scopes |
| `methods` | `list[str]` | Apply to specific methods |

## Examples

### Public and Private Routes

```python
app.add_middleware(
    RouteAuthMiddleware,
    routes=[
        RouteAuth("/api/public/*", require_auth=False),
        RouteAuth("/api/private/*", require_auth=True),
    ],
)

```

### Role-Based Access

```python
app.add_middleware(
    RouteAuthMiddleware,
    routes=[
        RouteAuth("/api/users", require_auth=True),
        RouteAuth("/api/users/*", require_auth=True),
        RouteAuth("/api/admin/*", require_auth=True, required_roles=["admin"]),
        RouteAuth("/api/superadmin/*", require_auth=True, required_roles=["superadmin"]),
    ],
)

```

### Method-Specific Rules

```python
app.add_middleware(
    RouteAuthMiddleware,
    routes=[
        # GET is public
        RouteAuth("/api/posts", require_auth=False, methods=["GET"]),
        # POST/PUT/DELETE require auth
        RouteAuth("/api/posts", require_auth=True, methods=["POST", "PUT", "DELETE"]),
    ],
)

```

### OAuth Scopes

```python
app.add_middleware(
    RouteAuthMiddleware,
    routes=[
        RouteAuth("/api/read/*", require_auth=True, required_scopes=["read"]),
        RouteAuth("/api/write/*", require_auth=True, required_scopes=["write"]),
        RouteAuth("/api/admin/*", require_auth=True, required_scopes=["admin"]),
    ],
)

```

### With Authentication Middleware

```python
from fastmiddleware import RouteAuthMiddleware, AuthenticationMiddleware, JWTAuthBackend

# Authentication first
app.add_middleware(
    AuthenticationMiddleware,
    backend=JWTAuthBackend(secret_key="..."),
    exclude_paths={"/api/public"},
)

# Route auth second
app.add_middleware(
    RouteAuthMiddleware,
    routes=[
        RouteAuth("/api/admin", required_roles=["admin"]),
    ],
)

```

### Default Require Auth

```python
app.add_middleware(
    RouteAuthMiddleware,
    default_require_auth=True,  # All routes need auth by default
    routes=[
        RouteAuth("/health", require_auth=False),
        RouteAuth("/docs", require_auth=False),
        RouteAuth("/api/public/*", require_auth=False),
    ],
)

```

## Error Responses

### Unauthenticated

```json
{
    "error": "Unauthorized",
    "detail": "Authentication required",
    "status_code": 401
}

```

### Insufficient Role

```json
{
    "error": "Forbidden",
    "detail": "Required role: admin",
    "status_code": 403
}

```

## Related Middlewares

- [AuthenticationMiddleware](authentication.md) - Authentication
- [ScopeMiddleware](scope.md) - OAuth scopes
- [BasicAuthMiddleware](basic-auth.md) - Basic auth
