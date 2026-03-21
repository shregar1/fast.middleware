# RequestPriorityMiddleware

Prioritize requests for processing.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestPriorityMiddleware, Priority

app = FastAPI()

app.add_middleware(
    RequestPriorityMiddleware,
    path_priorities={
        "/api/health": Priority.CRITICAL,
        "/api/webhooks": Priority.HIGH,
        "/api/reports": Priority.LOW,
    },
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `path_priorities` | `dict[str, Priority]` | `{}` | Priority by path |
| `default_priority` | `Priority` | `NORMAL` | Default priority |
| `header_name` | `str` | `"X-Priority"` | Priority header |

## Priority Levels

| Level | Value | Use Case |
| ------- | ------- | ---------- |
| `CRITICAL` | 0 | Health checks, monitoring |
| `HIGH` | 1 | Webhooks, real-time |
| `NORMAL` | 2 | Regular API calls |
| `LOW` | 3 | Reports, batch jobs |
| `BACKGROUND` | 4 | Analytics, non-urgent |

## Examples

### Path-Based Priorities

```python
app.add_middleware(
    RequestPriorityMiddleware,
    path_priorities={
        "/api/health": Priority.CRITICAL,
        "/api/live": Priority.CRITICAL,
        "/api/webhooks/*": Priority.HIGH,
        "/api/reports/*": Priority.LOW,
        "/api/export": Priority.BACKGROUND,
    },
)

```

### Client-Specified Priority

```python
app.add_middleware(
    RequestPriorityMiddleware,
    header_name="X-Request-Priority",
)

# Client can send: X-Request-Priority: high

```

### With Load Shedding

```python
from fastmiddleware import RequestPriorityMiddleware, LoadSheddingMiddleware

# Priority first
app.add_middleware(
    RequestPriorityMiddleware,
    path_priorities={"/api/health": Priority.CRITICAL},
)

# Load shedding respects priority
app.add_middleware(
    LoadSheddingMiddleware,
    max_concurrent=1000,
    shed_low_priority_first=True,
)

```

### Dynamic Priority

```python
from fastmiddleware import RequestPriorityMiddleware

class DynamicPriority(RequestPriorityMiddleware):
    async def get_priority(self, request) -> Priority:
        # Premium users get higher priority
        if request.state.user_tier == "premium":
            return Priority.HIGH

        # Path-based
        if request.url.path.startswith("/api/webhooks"):
            return Priority.HIGH

        return Priority.NORMAL

app.add_middleware(DynamicPriority)

```

### Queue Integration

```python
from fastmiddleware import RequestPriorityMiddleware, Priority

@app.post("/tasks")
async def create_task(task: Task, request: Request):
    priority = getattr(request.state, "priority", Priority.NORMAL)

    # Use priority for queue ordering
    await task_queue.enqueue(task, priority=priority.value)

    return {"queued": True, "priority": priority.name}

```

## Request State

```python
request.state.priority  # Priority enum value

```

## Response Headers

```http
X-Priority: HIGH
X-Priority-Value: 1

```

## Use Cases

1. **High Availability** - Keep health checks responsive
2. **Fair Scheduling** - Balance request processing
3. **SLA Management** - Prioritize premium customers
4. **Graceful Degradation** - Shed low priority first

## Related Middlewares

- [LoadSheddingMiddleware](load-shedding.md) - Load shedding
- [BulkheadMiddleware](bulkhead.md) - Bulkhead pattern
- [RateLimitMiddleware](rate-limit.md) - Rate limiting
