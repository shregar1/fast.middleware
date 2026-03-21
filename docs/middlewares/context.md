# ContextMiddleware

Shared async-safe request context for storing and retrieving values.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ContextMiddleware, get_context_value, set_context_value

app = FastAPI()

app.add_middleware(
    ContextMiddleware,
    extract_headers={"X-User-ID": "user_id", "X-Tenant-ID": "tenant_id"},
)

@app.get("/")
async def handler():
    user_id = get_context_value("user_id")
    set_context_value("processed", True)
    return {"user_id": user_id}

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `extract_headers` | `dict[str, str]` | `{}` | Map headers to context keys |
| `extract_query` | `dict[str, str]` | `{}` | Map query params to context keys |

## Helper Functions

### `get_context() -> dict`

Returns the full context dictionary.

```python
from fastmiddleware import get_context

ctx = get_context()
print(ctx)  # {"user_id": "123", "tenant_id": "acme", ...}

```

### `get_context_value(key, default=None) -> Any`

Get a specific context value.

```python
from fastmiddleware import get_context_value

user_id = get_context_value("user_id")
tier = get_context_value("tier", default="free")

```

### `set_context_value(key, value) -> None`

Set a context value (available for rest of request).

```python
from fastmiddleware import set_context_value

set_context_value("authenticated", True)
set_context_value("permissions", ["read", "write"])

```

## Examples

### Extract Headers to Context

```python
app.add_middleware(
    ContextMiddleware,
    extract_headers={
        "X-User-ID": "user_id",
        "X-Request-ID": "request_id",
        "X-Tenant-ID": "tenant_id",
    },
)

@app.get("/profile")
async def profile():
    user_id = get_context_value("user_id")
    return await db.get_user(user_id)

```

### Setting Context in Middleware Chain

```python
from fastmiddleware import ContextMiddleware, set_context_value

# In auth middleware
@app.middleware("http")
async def auth_middleware(request, call_next):
    user = await authenticate(request)
    set_context_value("user", user)
    set_context_value("permissions", user.permissions)
    return await call_next(request)

# In route handler
@app.get("/protected")
async def protected():
    user = get_context_value("user")
    permissions = get_context_value("permissions")
    return {"user": user.name, "permissions": permissions}

```

### Context in Background Tasks

```python
from fastmiddleware import get_context

@app.post("/process")
async def process(background_tasks: BackgroundTasks):
    ctx = get_context()  # Capture context

    async def background_work():
        # Context is available in background task
        user_id = ctx.get("user_id")
        await do_work(user_id)

    background_tasks.add_task(background_work)
    return {"status": "processing"}

```

### Logging with Context

```python
import logging
from fastmiddleware import get_context_value

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.user_id = get_context_value("user_id", "anonymous")
        record.request_id = get_context_value("request_id", "unknown")
        return True

logger = logging.getLogger(__name__)
logger.addFilter(ContextFilter())

# Log format: [%(request_id)s] [%(user_id)s] %(message)s

```

## Thread/Async Safety

The context uses `contextvars.ContextVar` internally, making it safe for:

- Async handlers

- Concurrent requests

- Background tasks (with proper context capture)

## Related Middlewares

- [RequestContextMiddleware](request-context.md) - Request ID context
- [CorrelationMiddleware](correlation.md) - Correlation IDs
- [TenantMiddleware](tenant.md) - Multi-tenancy context
