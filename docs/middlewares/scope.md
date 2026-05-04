# ScopeMiddleware

OAuth scope validation for routes.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ScopeMiddleware

app = FastAPI()

app.add_middleware(
    ScopeMiddleware,
    route_scopes={
        "/api/users": ["users:read"],
        "/api/users/create": ["users:write"],
        "/api/admin": ["admin:all"],
    },
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `route_scopes` | `dict[str, list[str]]` | `{}` | Required scopes by path |
| `require_all` | `bool` | `False` | Require all scopes vs any |
| `scope_key` | `str` | `"scopes"` | Key in request.state |

## Examples

### Basic Scope Validation

```python
app.add_middleware(
    ScopeMiddleware,
    route_scopes={
        "/api/users": ["users:read"],
        "/api/orders": ["orders:read"],
    },
)

# Request with scopes=["users:read"] can access /api/users

# Request with scopes=["orders:read"] cannot access /api/users

```

### Require Any Scope

```python
app.add_middleware(
    ScopeMiddleware,
    route_scopes={
        "/api/users": ["users:read", "admin:all"],
    },
    require_all=False,  # Any scope is sufficient
)

# User with "admin:all" can access /api/users

```

### Require All Scopes

```python
app.add_middleware(
    ScopeMiddleware,
    route_scopes={
        "/api/sensitive": ["verified", "premium", "mfa"],
    },
    require_all=True,  # All scopes required
)

# User must have ALL three scopes

```

### With Authentication

```python
from fastmiddleware import ScopeMiddleware, AuthenticationMiddleware, JWTAuthBackend

# JWT auth extracts scopes from token
app.add_middleware(
    AuthenticationMiddleware,
    backend=JWTAuthBackend(secret_key="..."),
)

# Scope middleware uses extracted scopes
app.add_middleware(
    ScopeMiddleware,
    route_scopes={
        "/api/users": ["users:read"],
    },
)

```

### Path Patterns

```python
app.add_middleware(
    ScopeMiddleware,
    route_scopes={
        "/api/users/*": ["users:read"],
        "/api/users/*/edit": ["users:write"],
        "/api/admin/*": ["admin:all"],
    },
)

```

### CRUD Scopes

```python
app.add_middleware(
    ScopeMiddleware,
    route_scopes={
        # Resource: users
        "GET /api/users": ["users:read"],
        "POST /api/users": ["users:write"],
        "PUT /api/users/*": ["users:write"],
        "DELETE /api/users/*": ["users:delete"],

        # Resource: orders
        "GET /api/orders": ["orders:read"],
        "POST /api/orders": ["orders:write"],
    },
)

```

### Custom Scope Source

```python
from fastmiddleware import ScopeMiddleware

class CustomScopeMiddleware(ScopeMiddleware):
    async def get_scopes(self, request) -> list[str]:
        # Get from custom location
        return request.state.permissions

app.add_middleware(
    CustomScopeMiddleware,
    route_scopes={...},
)

```

## Error Response

```json
{
    "error": "Forbidden",
    "detail": "Missing required scope: users:write",
    "required": ["users:write"],
    "provided": ["users:read"],
    "status_code": 403
}

```

## Related Middlewares

- [AuthenticationMiddleware](authentication.md) - Authentication
- [RouteAuthMiddleware](route-auth.md) - Per-route auth
- [BearerAuthMiddleware](bearer-auth.md) - Bearer tokens
