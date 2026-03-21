# BasicAuthMiddleware

HTTP Basic Authentication middleware.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import BasicAuthMiddleware, BasicAuthConfig

app = FastAPI()

# Basic usage
app.add_middleware(
    BasicAuthMiddleware,
    users={"admin": "secret123", "user": "password"},
)

# With config
config = BasicAuthConfig(
    users={"admin": "secret123"},
    realm="My API",
    exclude_methods={"OPTIONS"},
)
app.add_middleware(BasicAuthMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `users` | `Dict[str, str]` | `{}` | Username to password mapping |
| `realm` | `str` | `"Restricted"` | Authentication realm |
| `exclude_methods` | `Set[str]` | `{"OPTIONS"}` | Methods that skip auth |
| `exclude_paths` | `Set[str]` | `set()` | Paths that skip auth |

## Client Usage

```bash

# curl
curl -u admin:secret123 https://api.example.com/protected

# With header
curl -H "Authorization: Basic YWRtaW46c2VjcmV0MTIz" https://api.example.com/protected

```

## Response Codes

| Code | Description |
| ------ | ------------- |
| 401 | Missing or invalid credentials |

## Response Headers

| Header | Value |
| -------- | ------- |
| `WWW-Authenticate` | `Basic realm="Restricted"` |

## Accessing User in Route

```python
@app.get("/")
async def handler(request: Request):
    username = request.state.user
    return {"user": username}

```

## Security Notes

⚠️ Basic auth transmits credentials in every request. Always use HTTPS!

## Related Middlewares

- [BearerAuthMiddleware](bearer-auth.md)
- [AuthenticationMiddleware](authentication.md)
