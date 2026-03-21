# ChaosMiddleware

Chaos engineering middleware for fault injection testing.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## ⚠️ Warning

**NEVER enable in production!** This middleware is for testing only.

## Usage

```python
from fastapi import FastAPI
import os
from fastmiddleware import ChaosMiddleware, ChaosConfig

app = FastAPI()

# Only enable in testing environments
app.add_middleware(
    ChaosMiddleware,
    enabled=os.getenv("CHAOS_ENABLED") == "true",
    failure_rate=0.1,    # 10% of requests fail
    latency_rate=0.2,    # 20% get extra latency
    min_latency=0.5,     # 500ms minimum
    max_latency=5.0,     # 5 seconds maximum
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `enabled` | `bool` | `False` | Must explicitly enable |
| `failure_rate` | `float` | `0.1` | Probability of failure (0-1) |
| `latency_rate` | `float` | `0.2` | Probability of latency (0-1) |
| `min_latency` | `float` | `0.1` | Min latency in seconds |
| `max_latency` | `float` | `5.0` | Max latency in seconds |
| `error_codes` | `List[int]` | `[500, 502, 503, 504]` | Error codes to return |
| `affected_paths` | `Set[str]` | `set()` | Paths to affect (empty = all) |

## What It Does

1. **Failure Injection**: Randomly returns 5xx errors
2. **Latency Injection**: Adds random delays
3. **Selective Targeting**: Can target specific paths

## Failure Response

```json
{
  "error": true,
  "message": "Chaos injection: 503",
  "chaos": true
}

```

## Testing Resilience

```python

# Test circuit breaker
config = ChaosConfig(
    enabled=True,
    failure_rate=0.5,  # 50% failures
)

# Test timeout handling
config = ChaosConfig(
    enabled=True,
    latency_rate=1.0,  # 100% get latency
    min_latency=10.0,
    max_latency=30.0,
)

# Test specific endpoints
config = ChaosConfig(
    enabled=True,
    failure_rate=0.3,
    affected_paths={"/api/external", "/api/database"},
)

```

## Safe Environment Check

```python

# Ensure chaos is never enabled in production
import os

if os.getenv("ENVIRONMENT") == "production":
    assert os.getenv("CHAOS_ENABLED") != "true", "Chaos must not be enabled in production!"

```

## Related Middlewares

- [SlowResponseMiddleware](slow-response.md) - Deterministic delays
- [CircuitBreakerMiddleware](circuit-breaker.md) - Test with chaos
