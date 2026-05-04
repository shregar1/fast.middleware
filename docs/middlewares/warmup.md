# WarmupMiddleware

Container warmup/readiness middleware for orchestration platforms.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import WarmupMiddleware, WarmupConfig

app = FastAPI()

# Basic usage
warmup = WarmupMiddleware(
    app,
    warmup_paths={"/_warmup", "/_ah/warmup"},
    min_warmup_time=5.0,  # 5 seconds
)

# Mark as ready after initialization
@app.on_event("startup")
async def startup():
    await initialize_database()
    await load_ml_model()
    warmup.set_ready(True)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `warmup_paths` | `Set[str]` | `{"/_warmup", "/_ah/warmup"}` | Warmup endpoints |
| `warmup_header` | `str` | `"X-Warmup"` | Header to indicate warmup |
| `min_warmup_time` | `float` | `0.0` | Minimum startup time |
| `ready` | `bool` | `True` | Initial ready state |

## How It Works

```text
App Starts ──> Warming Up ──> Ready
                  │              │
                  ▼              ▼
         Returns 503       Returns 200
         for all requests  for all requests

```

## Warmup Endpoint Response

```json
// GET /_warmup
{
  "ready": true,
  "uptime": 5.234,
  "warmup_time": 5.0
}

```

## Kubernetes Integration

```yaml

# Deployment with readiness probe
spec:
  containers:
    - name: api
      readinessProbe:
        httpGet:
          path: /_warmup
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 5

```

## Google App Engine

Uses `/_ah/warmup` automatically:

```yaml

# app.yaml
inbound_services:
  - warmup

```

## Manual Control

```python

# Set not ready (for maintenance)
warmup.set_ready(False)

# Check status
if warmup._is_ready():
    print("Ready to serve traffic")

```

## Response Codes

| Path | Status | Description |
| ------ | -------- | ------------- |
| `/_warmup` | 200 | Ready |
| `/_warmup` | 503 | Still warming up |
| Other paths | 503 | During warmup |

## Related Middlewares

- [HealthCheckMiddleware](health.md)
- [GracefulShutdownMiddleware](graceful-shutdown.md)
- [MaintenanceMiddleware](maintenance.md)
