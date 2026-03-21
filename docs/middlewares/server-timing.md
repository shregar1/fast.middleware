# ServerTimingMiddleware

Server-Timing header for browser devtools integration.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import ServerTimingMiddleware, timing, add_timing

app = FastAPI()

app.add_middleware(ServerTimingMiddleware)

@app.get("/")
async def handler():
    # Using context manager
    with timing("db", "Database query"):
        result = await db.query(...)

    with timing("cache", "Cache lookup"):
        cached = await cache.get(...)

    with timing("render"):
        output = render(result)

    return output

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `include_total` | `bool` | `True` | Include total time |
| `include_app` | `bool` | `True` | Include app processing time |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## Adding Timings

### Context Manager

```python
with timing("operation_name", "Description"):
    # Code to time
    pass

```

### Manual

```python
from fastmiddleware import add_timing
import time

start = time.perf_counter()
await do_something()
duration = (time.perf_counter() - start) * 1000

add_timing("operation", duration, "Description")

```

## Response Header

```http
Server-Timing: db;dur=45.23;desc="Database query", cache;dur=2.15;desc="Cache lookup", render;dur=12.45, total;dur=65.12

```

## Browser DevTools

The Server-Timing header is visible in browser DevTools:

- Chrome: Network tab → Select request → Timing

- Firefox: Network tab → Timings

## Nested Timings

```python
@app.get("/complex")
async def complex_handler():
    with timing("total", "Total processing"):
        with timing("fetch", "Fetch data"):
            data = await fetch_data()

        with timing("transform", "Transform data"):
            result = transform(data)

        with timing("validate", "Validate result"):
            validate(result)

    return result

```

## Best Practices

1. Use descriptive names and descriptions
2. Time external calls (DB, APIs, cache)
3. Don't expose sensitive timing info in production
4. Keep timing overhead minimal

## Related Middlewares

- [TimingMiddleware](timing.md) - Simple X-Process-Time header
- [ProfilingMiddleware](profiling.md) - Detailed profiling
- [ResponseTimeMiddleware](response-time.md) - SLA monitoring
