# DeprecationMiddleware

Add deprecation warnings to API endpoints.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import DeprecationMiddleware, DeprecationInfo

app = FastAPI()

app.add_middleware(
    DeprecationMiddleware,
    deprecations=[
        DeprecationInfo(
            path="/api/v1/users",
            sunset_date="2025-12-31",
            replacement="/api/v2/users",
        ),
    ],
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `deprecations` | `list[DeprecationInfo]` | `[]` | Deprecation definitions |

## DeprecationInfo Fields

| Field | Type | Description |
| ------- | ------ | ------------- |
| `path` | `str` | Path pattern to deprecate |
| `sunset_date` | `str` | Date when endpoint is removed |
| `replacement` | `str` | New endpoint to use |
| `message` | `str` | Custom deprecation message |

## Response Headers

```http
Deprecation: true
Sunset: Wed, 31 Dec 2025 00:00:00 GMT
Link: </api/v2/users>; rel="successor-version"
X-Deprecation-Notice: This endpoint is deprecated. Use /api/v2/users instead.

```

## Examples

### Basic Deprecation

```python
app.add_middleware(
    DeprecationMiddleware,
    deprecations=[
        DeprecationInfo(
            path="/api/v1/users",
            sunset_date="2025-12-31",
            replacement="/api/v2/users",
        ),
    ],
)

```

### Multiple Deprecations

```python
app.add_middleware(
    DeprecationMiddleware,
    deprecations=[
        DeprecationInfo(
            path="/api/v1/users",
            sunset_date="2025-06-30",
            replacement="/api/v2/users",
        ),
        DeprecationInfo(
            path="/api/v1/orders",
            sunset_date="2025-06-30",
            replacement="/api/v2/orders",
        ),
        DeprecationInfo(
            path="/legacy/*",
            sunset_date="2025-03-01",
            message="Legacy API is being removed",
        ),
    ],
)

```

### Custom Message

```python
app.add_middleware(
    DeprecationMiddleware,
    deprecations=[
        DeprecationInfo(
            path="/api/search",
            sunset_date="2025-12-31",
            message="Please migrate to the new GraphQL API at /graphql",
        ),
    ],
)

```

### Path Pattern Matching

```python
app.add_middleware(
    DeprecationMiddleware,
    deprecations=[
        # Exact match
        DeprecationInfo(path="/api/v1/users", ...),

        # Wildcard
        DeprecationInfo(path="/api/v1/*", ...),

        # Regex pattern
        DeprecationInfo(path=r"/api/v1/users/\d+", ...),
    ],
)

```

### With Version Header

```python
from fastmiddleware import DeprecationMiddleware, APIVersionHeaderMiddleware

app.add_middleware(
    APIVersionHeaderMiddleware,
    version="2.0.0",
    min_version="1.0.0",
)

app.add_middleware(
    DeprecationMiddleware,
    deprecations=[
        DeprecationInfo(
            path="/api/v1/*",
            sunset_date="2025-12-31",
            replacement="/api/v2/{path}",
        ),
    ],
)

```

## Client Handling

Clients should watch for:

- `Deprecation: true` header

- `Sunset` header for removal date

- `Link` header with `rel="successor-version"`

```javascript
if (response.headers.get('Deprecation') === 'true') {
    console.warn('API endpoint deprecated:', response.headers.get('X-Deprecation-Notice'));
    console.warn('Sunset date:', response.headers.get('Sunset'));
}

```

## Related Middlewares

- [APIVersionHeaderMiddleware](api-version-header.md) - Version headers
- [VersioningMiddleware](versioning.md) - API versioning
- [RedirectMiddleware](redirect.md) - URL redirects
