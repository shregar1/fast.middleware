# CorrelationMiddleware

Correlation ID middleware for distributed tracing.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import CorrelationMiddleware, CorrelationConfig, get_correlation_id

app = FastAPI()

# Basic usage
app.add_middleware(CorrelationMiddleware)

# With config
config = CorrelationConfig(
    header_name="X-Correlation-ID",
    generate_if_missing=True,
)
app.add_middleware(CorrelationMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `header_name` | `str` | `"X-Correlation-ID"` | Header name |
| `generate_if_missing` | `bool` | `True` | Generate ID if not present |
| `include_in_response` | `bool` | `True` | Add to response headers |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## Getting Correlation ID

```python
from fastmiddleware import get_correlation_id

@app.get("/")
async def handler():
    correlation_id = get_correlation_id()

    # Include in logs
    logger.info(f"Processing request", extra={"correlation_id": correlation_id})

    return {"correlation_id": correlation_id}

```

## Propagation to Downstream Services

```python
import httpx
from fastmiddleware import get_correlation_id

@app.get("/aggregate")
async def aggregate():
    correlation_id = get_correlation_id()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://service-b/data",
            headers={"X-Correlation-ID": correlation_id},
        )

    return response.json()

```

## Structured Logging

```python
import logging
import json

class CorrelationFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = get_correlation_id() or "unknown"
        return True

logger = logging.getLogger()
logger.addFilter(CorrelationFilter())

formatter = logging.Formatter(
    '{"correlation_id": "%(correlation_id)s", "message": "%(message)s"}'
)

```

## Response Headers

| Header | Value |
| -------- | ------- |
| `X-Correlation-ID` | The correlation ID |

## Client Usage

```bash

# Provide your own ID
curl -H "X-Correlation-ID: my-request-123" https://api.example.com/

# Or let the server generate one
curl https://api.example.com/

# Response includes: X-Correlation-ID: <generated-uuid>

```

## Related Middlewares

- [RequestIDMiddleware](request-id.md) - Request ID generation
- [RequestIDPropagationMiddleware](request-id-propagation.md) - ID chain propagation
- [LoggingMiddleware](logging.md)
