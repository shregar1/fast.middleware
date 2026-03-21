# BearerAuthMiddleware

Bearer token authentication middleware.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import BearerAuthMiddleware, BearerAuthConfig

app = FastAPI()

# With static tokens
app.add_middleware(
    BearerAuthMiddleware,
    tokens={
        "token123": {"user_id": 1, "role": "admin"},
        "token456": {"user_id": 2, "role": "user"},
    },
)

# With custom validation
middleware = BearerAuthMiddleware(app)

async def validate_token(token: str):
    user = await db.get_user_by_token(token)
    return {"user_id": user.id, "role": user.role} if user else None

middleware.set_validate_func(validate_token)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `tokens` | `Dict[str, Dict]` | `{}` | Token to user info mapping |
| `header_name` | `str` | `"Authorization"` | Header name |
| `realm` | `str` | `"API"` | Authentication realm |
| `return_error_detail` | `bool` | `False` | Include error details |
| `exclude_paths` | `Set[str]` | `set()` | Paths to skip auth |

## Client Usage

```bash
curl -H "Authorization: Bearer token123" https://api.example.com/protected

```

## Response Codes

| Code | Description |
| ------ | ------------- |
| 401 | Missing or invalid token |

## Accessing User in Route

```python
@app.get("/")
async def handler(request: Request):
    user = request.state.user  # {"user_id": 1, "role": "admin"}
    token = request.state.token  # "token123"
    return {"user_id": user["user_id"]}

```

## Related Middlewares

- [BasicAuthMiddleware](basic-auth.md)
- [AuthenticationMiddleware](authentication.md) - JWT support
