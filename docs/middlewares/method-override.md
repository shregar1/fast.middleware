# MethodOverrideMiddleware

Override HTTP methods via header or query parameter.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import MethodOverrideMiddleware

app = FastAPI()

app.add_middleware(MethodOverrideMiddleware)

```

## How It Works

Allows clients to override HTTP methods when they can only send GET/POST:

- `POST /resource?_method=DELETE` → `DELETE /resource`

- `POST /resource` with `X-HTTP-Method-Override: PUT` → `PUT /resource`

## Configuration

|Parameter|Type|Default|Description|
| ----------- | ------ | --------- | ------------- |
|`query_param`|`str`|`"_method"`|Query parameter name|
|`header_name`|`str`|`"X-HTTP-Method-Override"`|Header name|
|`allowed_methods`|`set[str]`|`{"PUT", "PATCH", "DELETE"}`|Methods that can be overridden to|

## Examples

### Basic Usage

```python
app.add_middleware(MethodOverrideMiddleware)

# POST /users/123?_method=DELETE

# Becomes: DELETE /users/123

```

### Via Header

```python

# POST /users/123

# X-HTTP-Method-Override: PUT

# Body: {"name": "Updated"}

# Becomes: PUT /users/123

```

### Custom Query Parameter

```python
app.add_middleware(
    MethodOverrideMiddleware,
    query_param="method",
)

# POST /users/123?method=DELETE

```

### Restrict Override Methods

```python
app.add_middleware(
    MethodOverrideMiddleware,
    allowed_methods={"DELETE"},  # Only allow DELETE override
)

# POST /users?_method=PUT → Rejected (405)

# POST /users?_method=DELETE → OK

```

### HTML Form Example

```html
<form action="/users/123" method="POST">
    <input type="hidden" name="_method" value="DELETE">
    <button type="submit">Delete User</button>
</form>

```

### With CSRF Protection

```python
from fastmiddleware import MethodOverrideMiddleware, CSRFMiddleware

# CSRF first (checks token)
app.add_middleware(CSRFMiddleware, secret_key="...")

# Method override after
app.add_middleware(MethodOverrideMiddleware)

```

## Use Cases

1. **HTML Forms** - Forms only support GET/POST
2. **Legacy Clients** - Clients that can't send PUT/DELETE
3. **Firewall Restrictions** - Some firewalls block non-GET/POST

## Security Considerations

- Only overrides POST requests (not GET)
- Header takes precedence over query parameter
- Should be used with CSRF protection

## Related Middlewares

- [CSRFMiddleware](csrf.md) - CSRF protection
- [RequestValidatorMiddleware](request-validator.md) - Request validation
