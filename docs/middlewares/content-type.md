# ContentTypeMiddleware

Validate and enforce Content-Type headers on requests.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ContentTypeMiddleware

app = FastAPI()

app.add_middleware(
    ContentTypeMiddleware,
    allowed_types=["application/json", "application/xml"],
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `allowed_types` | `list[str]` | `["application/json"]` | Allowed content types |
| `methods` | `list[str]` | `["POST", "PUT", "PATCH"]` | Methods to validate |
| `strict` | `bool` | `True` | Require exact match vs prefix |

## Examples

### JSON Only

```python
app.add_middleware(
    ContentTypeMiddleware,
    allowed_types=["application/json"],
)

# POST with Content-Type: text/plain -> 415 Unsupported Media Type

# POST with Content-Type: application/json -> OK

```

### Multiple Types

```python
app.add_middleware(
    ContentTypeMiddleware,
    allowed_types=[
        "application/json",
        "application/xml",
        "multipart/form-data",
    ],
)

```

### With Charset Variants

```python
app.add_middleware(
    ContentTypeMiddleware,
    allowed_types=["application/json"],
    strict=False,  # Allows application/json; charset=utf-8
)

```

### File Upload Endpoint

```python
app.add_middleware(
    ContentTypeMiddleware,
    allowed_types=[
        "application/json",
        "multipart/form-data",
        "application/octet-stream",
    ],
)

```

### Exclude Certain Paths

```python
from fastmiddleware import ContentTypeMiddleware, ContentTypeConfig

config = ContentTypeConfig(
    allowed_types=["application/json"],
    exclude_paths={"/upload", "/webhook"},
)

app.add_middleware(ContentTypeMiddleware, config=config)

```

## Error Response

When an invalid Content-Type is received:

```json
{
    "error": "Unsupported Media Type",
    "detail": "Content-Type 'text/plain' is not supported. Allowed types: application/json, application/xml",
    "status_code": 415
}

```

## Use Cases

1. **API Security** - Prevent unexpected content types
2. **Input Validation** - Ensure proper data format
3. **Standards Compliance** - Enforce API contract

## Related Middlewares

- [RequestValidatorMiddleware](request-validator.md) - Full request validation
- [JSONSchemaMiddleware](json-schema.md) - JSON Schema validation
- [PayloadSizeMiddleware](payload-size.md) - Size limits
