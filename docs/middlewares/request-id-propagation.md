# RequestIDPropagationMiddleware

Propagate request IDs across service boundaries.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestIDPropagationMiddleware, get_request_ids

app = FastAPI()

app.add_middleware(RequestIDPropagationMiddleware)

@app.get("/")
async def handler():
    ids = get_request_ids()
    return {"trace": ids}

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `header_name` | `str` | `"X-Request-ID"` | Request ID header |
| `trace_header` | `str` | `"X-Trace-ID"` | Trace chain header |
| `separator` | `str` | `","` | ID separator |

## Helper Functions

### `get_request_ids() -> list[str]`

Returns the chain of request IDs from upstream services.

```python
from fastmiddleware import get_request_ids

@app.get("/")
async def handler():
    ids = get_request_ids()
    # ["original-id", "gateway-id", "service-id"]
    return {"trace_chain": ids}

```

### `get_trace_header() -> str`

Returns the full trace header for forwarding.

```python
from fastmiddleware import get_trace_header

@app.get("/downstream")
async def call_downstream():
    headers = {"X-Trace-ID": get_trace_header()}
    response = await httpx.get("http://other-service/api", headers=headers)
    return response.json()

```

## Examples

### Basic Propagation

```python
app.add_middleware(RequestIDPropagationMiddleware)

# Incoming: X-Request-ID: abc-123

# Adds: X-Trace-ID: abc-123,def-456 (original + new)

```

### Custom Header Names

```python
app.add_middleware(
    RequestIDPropagationMiddleware,
    header_name="X-Correlation-ID",
    trace_header="X-B3-TraceId",
)

```

### Forward to Downstream Services

```python
import httpx
from fastmiddleware import get_trace_header, get_request_ids

@app.get("/aggregate")
async def aggregate():
    trace = get_trace_header()

    async with httpx.AsyncClient() as client:
        # Forward trace to downstream services
        headers = {"X-Trace-ID": trace}

        users = await client.get("http://users-service/api", headers=headers)
        orders = await client.get("http://orders-service/api", headers=headers)

    return {
        "users": users.json(),
        "orders": orders.json(),
        "trace_chain": get_request_ids(),
    }

```

### Logging with Trace

```python
import logging
from fastmiddleware import get_request_ids

class TraceFilter(logging.Filter):
    def filter(self, record):
        ids = get_request_ids()
        record.trace_id = ids[0] if ids else "unknown"
        record.span_id = ids[-1] if ids else "unknown"
        return True

# All logs include trace_id and span_id

```

### OpenTelemetry Integration

```python
from fastmiddleware import get_request_ids
from opentelemetry import trace

@app.get("/traced")
async def traced():
    request_ids = get_request_ids()

    # Set trace context
    current_span = trace.get_current_span()
    current_span.set_attribute("request.trace_chain", request_ids)

    return {"traced": True}

```

## Header Flow

```text
Client → Gateway → Service A → Service B

Client:
  X-Request-ID: abc

Gateway:
  Receives: X-Request-ID: abc
  Forwards: X-Trace-ID: abc,gw-123

Service A:
  Receives: X-Trace-ID: abc,gw-123
  Forwards: X-Trace-ID: abc,gw-123,svc-a-456

Service B:
  Receives: X-Trace-ID: abc,gw-123,svc-a-456
  get_request_ids() → ["abc", "gw-123", "svc-a-456", "svc-b-789"]

```

## Related Middlewares

- [RequestIDMiddleware](request-id.md) - Generate request IDs
- [CorrelationMiddleware](correlation.md) - Correlation IDs
- [RequestContextMiddleware](request-context.md) - Request context
