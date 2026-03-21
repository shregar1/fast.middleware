# ResponseFormatMiddleware

Standardize response format across all endpoints.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ResponseFormatMiddleware

app = FastAPI()

app.add_middleware(
    ResponseFormatMiddleware,
    wrap_responses=True,
    success_key="data",
    error_key="error",
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `wrap_responses` | `bool` | `True` | Wrap all responses |
| `success_key` | `str` | `"data"` | Key for successful data |
| `error_key` | `str` | `"error"` | Key for error details |
| `include_metadata` | `bool` | `True` | Include metadata |

## Response Format

### Success Response

```json
{
    "data": {
        "id": 123,
        "name": "John"
    },
    "metadata": {
        "request_id": "abc-123",
        "timestamp": "2025-01-18T10:30:00Z",
        "duration_ms": 45.2
    }
}

```

### Error Response

```json
{
    "error": {
        "code": "NOT_FOUND",
        "message": "User not found",
        "details": {}
    },
    "metadata": {
        "request_id": "abc-123",
        "timestamp": "2025-01-18T10:30:00Z"
    }
}

```

## Examples

### Basic Wrapping

```python
app.add_middleware(
    ResponseFormatMiddleware,
    wrap_responses=True,
)

@app.get("/user")
async def get_user():
    return {"id": 1, "name": "John"}

# Response:

# {"data": {"id": 1, "name": "John"}, "metadata": {...}}

```

### Without Metadata

```python
app.add_middleware(
    ResponseFormatMiddleware,
    wrap_responses=True,
    include_metadata=False,
)

# Response:

# {"data": {"id": 1, "name": "John"}}

```

### Custom Keys

```python
app.add_middleware(
    ResponseFormatMiddleware,
    success_key="result",
    error_key="fault",
)

# Response:

# {"result": {...}, "metadata": {...}}

```

### Exclude Paths

```python
from fastmiddleware import ResponseFormatMiddleware, ResponseFormatConfig

config = ResponseFormatConfig(
    wrap_responses=True,
    exclude_paths={"/health", "/metrics", "/docs"},
)

app.add_middleware(ResponseFormatMiddleware, config=config)

```

### With Pagination

```python
@app.get("/users")
async def list_users(page: int = 1, limit: int = 10):
    users = await db.get_users(page, limit)
    total = await db.count_users()

    return {
        "items": users,
        "page": page,
        "limit": limit,
        "total": total,
    }

# Response:

# {

#     "data": {

#         "items": [...],

#         "page": 1,

#         "limit": 10,

#         "total": 100

#     },

#     "metadata": {...}

# }

```

### Custom Metadata

```python
from fastmiddleware import ResponseFormatMiddleware

class CustomFormatMiddleware(ResponseFormatMiddleware):
    def get_metadata(self, request, response, duration):
        return {
            "request_id": request.state.request_id,
            "api_version": "2.0",
            "duration_ms": duration,
            "rate_limit_remaining": request.state.rate_limit_remaining,
        }

app.add_middleware(CustomFormatMiddleware)

```

## Use Cases

1. **API Consistency** - Uniform response structure
2. **Client SDKs** - Predictable parsing
3. **Error Handling** - Consistent error format
4. **Debugging** - Built-in request metadata

## Related Middlewares

- [ErrorHandlerMiddleware](error-handler.md) - Error formatting
- [RequestIDMiddleware](request-id.md) - Request IDs
- [TimingMiddleware](timing.md) - Response timing
