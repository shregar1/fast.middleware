# VersioningMiddleware

API versioning middleware supporting header, query, and path-based versions.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import VersioningMiddleware, VersioningConfig, VersionLocation, get_api_version

app = FastAPI()

# Header-based versioning
app.add_middleware(
    VersioningMiddleware,
    default_version="1.0",
    location=VersionLocation.HEADER,
    header_name="X-API-Version",
)

# Query-based versioning
app.add_middleware(
    VersioningMiddleware,
    default_version="1.0",
    location=VersionLocation.QUERY,
    query_param="version",
)

# Path-based versioning
app.add_middleware(
    VersioningMiddleware,
    default_version="1.0",
    location=VersionLocation.PATH,
    path_prefix="/v",  # Matches /v1, /v2, etc.
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `default_version` | `str` | `"1.0"` | Default API version |
| `location` | `VersionLocation` | `HEADER` | Where to find version |
| `header_name` | `str` | `"X-API-Version"` | Header name |
| `query_param` | `str` | `"version"` | Query parameter name |
| `path_prefix` | `str` | `"/v"` | Path prefix for version |
| `supported_versions` | `Set[str]` | `set()` | Supported versions (empty = all) |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## Getting Version

```python
from fastmiddleware import get_api_version

@app.get("/users")
async def get_users():
    version = get_api_version()

    if version == "2.0":
        return get_users_v2()
    return get_users_v1()

# Or from request state
@app.get("/data")
async def get_data(request: Request):
    version = request.state.api_version
    return {"version": version}

```

## Version Locations

### Header (Recommended)

```bash
curl -H "X-API-Version: 2.0" https://api.example.com/users

```

### Query Parameter

```bash
curl "https://api.example.com/users?version=2.0"

```

### URL Path

```bash
curl https://api.example.com/v2/users

```

## Response Headers

| Header | Value |
| -------- | ------- |
| `X-API-Version` | Current API version |

## Unsupported Version

If `supported_versions` is set and version not in list:

```json
{
  "error": true,
  "message": "Unsupported API version: 3.0",
  "supported_versions": ["1.0", "2.0"]
}

```

## Related Middlewares

- [DeprecationMiddleware](deprecation.md) - Version deprecation
- [APIVersionHeaderMiddleware](api-version-header.md)
