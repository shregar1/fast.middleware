# APIVersionHeaderMiddleware

Add API version information to all response headers.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import APIVersionHeaderMiddleware

app = FastAPI()

app.add_middleware(
    APIVersionHeaderMiddleware,
    version="2.1.0",
    min_version="1.5.0",
)

```

## Configuration

| Parameter | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| `version` | `str` | Required | Current API version |
| `min_version` | `str` | `None` | Minimum supported version |
| `sunset_date` | `str` | `None` | Date when older versions sunset |
| `header_name` | `str` | `"X-API-Version"` | Response header name |

## Response Headers

The middleware adds these headers to all responses:

```http
X-API-Version: 2.1.0
X-API-Min-Version: 1.5.0
Sunset: Sat, 31 Dec 2025 23:59:59 GMT

```

## Examples

### Basic Usage

```python
app.add_middleware(
    APIVersionHeaderMiddleware,
    version="2.1.0",
)

# All responses include:

# X-API-Version: 2.1.0

```

### With Sunset Date

```python
app.add_middleware(
    APIVersionHeaderMiddleware,
    version="3.0.0",
    min_version="2.0.0",
    sunset_date="2025-12-31",
)

# Responses include:

# X-API-Version: 3.0.0

# X-API-Min-Version: 2.0.0

# Sunset: Wed, 31 Dec 2025 00:00:00 GMT

```

### Custom Header Name

```python
app.add_middleware(
    APIVersionHeaderMiddleware,
    version="1.0.0",
    header_name="X-Service-Version",
)

```

## Use Cases

1. **Client SDK Version Checking** - Clients can check if they need to update
2. **API Gateway Routing** - Route requests based on version headers
3. **Deprecation Notices** - Communicate upcoming changes via sunset headers
4. **Debugging** - Identify which API version handled a request

## Related Middlewares

- [VersioningMiddleware](versioning.md) - Full API versioning with routing
- [DeprecationMiddleware](deprecation.md) - Deprecation warnings for endpoints
