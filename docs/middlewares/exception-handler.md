# ExceptionHandlerMiddleware

Custom exception handling with registered handlers.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastmiddleware import ExceptionHandlerMiddleware

app = FastAPI()

handler = ExceptionHandlerMiddleware(app, debug=False)

@handler.register(ValueError)
def handle_value_error(exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid value", "detail": str(exc)}
    )

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `debug` | `bool` | `False` | Include tracebacks in responses |

## Examples

### Register Multiple Handlers

```python
handler = ExceptionHandlerMiddleware(app)

@handler.register(ValueError)
def handle_value_error(exc):
    return JSONResponse(status_code=400, content={"error": str(exc)})

@handler.register(KeyError)
def handle_key_error(exc):
    return JSONResponse(status_code=404, content={"error": f"Not found: {exc}"})

@handler.register(PermissionError)
def handle_permission_error(exc):
    return JSONResponse(status_code=403, content={"error": "Forbidden"})

```

### Custom Exception Classes

```python
class NotFoundError(Exception):
    def __init__(self, resource: str, id: str):
        self.resource = resource
        self.id = id

class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message

handler = ExceptionHandlerMiddleware(app)

@handler.register(NotFoundError)
def handle_not_found(exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "resource": exc.resource,
            "id": exc.id,
        }
    )

@handler.register(ValidationError)
def handle_validation(exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "field": exc.field,
            "message": exc.message,
        }
    )

```

### Debug Mode

```python

# Development
handler = ExceptionHandlerMiddleware(app, debug=True)

# Response includes traceback:

# {

#     "error": "ValueError",

#     "detail": "...",

#     "traceback": ["..."]

# }

# Production
handler = ExceptionHandlerMiddleware(app, debug=False)

# Response excludes traceback:

# {"error": "ValueError", "detail": "..."}

```

### Async Handlers

```python
@handler.register(DatabaseError)
async def handle_db_error(exc: DatabaseError):
    await log_error(exc)
    await notify_oncall(exc)

    return JSONResponse(
        status_code=503,
        content={"error": "Service temporarily unavailable"}
    )

```

### Exception Hierarchy

```python
class APIError(Exception):
    pass

class AuthError(APIError):
    pass

class RateLimitError(APIError):
    pass

# Handler for base class catches all subclasses
@handler.register(APIError)
def handle_api_error(exc: APIError):
    return JSONResponse(status_code=500, content={"error": str(exc)})

# More specific handler takes precedence
@handler.register(AuthError)
def handle_auth_error(exc: AuthError):
    return JSONResponse(status_code=401, content={"error": "Unauthorized"})

```

### Logging Exceptions

```python
import logging

logger = logging.getLogger(__name__)

@handler.register(Exception)
def handle_all(exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

```

## Related Middlewares

- [ErrorHandlerMiddleware](error-handler.md) - Standard error formatting
- [CircuitBreakerMiddleware](circuit-breaker.md) - Circuit breaker pattern
