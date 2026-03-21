# GracefulShutdownMiddleware

Graceful shutdown with request draining.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import GracefulShutdownMiddleware

app = FastAPI()

# Basic usage
shutdown_mw = GracefulShutdownMiddleware(app, timeout=30.0)

# With signal handling
import signal
import asyncio

async def shutdown_handler():
    await shutdown_mw.shutdown()
    # Additional cleanup...

@app.on_event("shutdown")
async def on_shutdown():
    await shutdown_mw.shutdown()

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `timeout` | `float` | `30.0` | Max drain time in seconds |
| `check_path` | `str` | `"/_shutdown"` | Status check endpoint |

## How It Works

1. **Normal operation**: Requests processed normally
2. **Shutdown initiated**: `shutdown()` called
3. **Draining**: New requests get 503, in-flight continue
4. **Complete**: All in-flight requests finished or timeout

```text
Normal ──> Shutdown Called ──> Draining ──> Complete
                                  │
                                  ▼
                         New requests: 503
                         In-flight: Continue

```

## Kubernetes Integration

```yaml

# Deployment with graceful shutdown
spec:
  terminationGracePeriodSeconds: 60
  containers:
    - name: api
      lifecycle:
        preStop:
          exec:
            command: ["/bin/sh", "-c", "sleep 5"]

```

## Health Check During Shutdown

```python
from fastmiddleware import HealthCheckMiddleware

# Health returns unhealthy during shutdown
@app.get("/health")
async def health():
    if shutdown_mw.is_shutting_down:
        return JSONResponse(
            status_code=503,
            content={"status": "shutting_down"},
        )
    return {"status": "healthy"}

```

## Monitoring

```python

# Check status
print(f"Shutting down: {shutdown_mw.is_shutting_down}")
print(f"In-flight requests: {shutdown_mw.in_flight_requests}")

# Status endpoint

# GET /_shutdown returns:

# {"shutting_down": true, "in_flight": 5}

```

## Related Middlewares

- [HealthCheckMiddleware](health.md)
- [WarmupMiddleware](warmup.md)
- [MaintenanceMiddleware](maintenance.md)
