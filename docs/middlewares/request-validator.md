# RequestValidatorMiddleware

Validate request structure and content.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestValidatorMiddleware, ValidationRule

app = FastAPI()

app.add_middleware(
    RequestValidatorMiddleware,
    rules=[
        ValidationRule(
            path="/api/upload",
            method="POST",
            required_headers=["Content-Type"],
            content_types=["multipart/form-data"],
            max_body_size=10 * 1024 * 1024,
        ),
    ],
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `rules` | `list[ValidationRule]` | `[]` | Validation rules |

## ValidationRule Fields

| Field | Type | Description |
| ------- | ------ | ------------- |
| `path` | `str` | Path pattern to match |
| `method` | `str` | HTTP method (or `"*"` for all) |
| `required_headers` | `list[str]` | Required headers |
| `content_types` | `list[str]` | Allowed content types |
| `max_body_size` | `int` | Maximum body size |
| `require_body` | `bool` | Body is required |

## Examples

### Validate Upload Endpoint

```python
app.add_middleware(
    RequestValidatorMiddleware,
    rules=[
        ValidationRule(
            path="/api/upload",
            method="POST",
            required_headers=["Content-Type", "Content-Length"],
            content_types=["multipart/form-data", "application/octet-stream"],
            max_body_size=50 * 1024 * 1024,  # 50 MB
        ),
    ],
)

```

### Validate JSON APIs

```python
app.add_middleware(
    RequestValidatorMiddleware,
    rules=[
        ValidationRule(
            path="/api/*",
            method="POST",
            content_types=["application/json"],
            require_body=True,
        ),
        ValidationRule(
            path="/api/*",
            method="PUT",
            content_types=["application/json"],
            require_body=True,
        ),
    ],
)

```

### Require Authorization

```python
app.add_middleware(
    RequestValidatorMiddleware,
    rules=[
        ValidationRule(
            path="/api/admin/*",
            method="*",
            required_headers=["Authorization"],
        ),
    ],
)

```

### Multiple Content Types

```python
app.add_middleware(
    RequestValidatorMiddleware,
    rules=[
        ValidationRule(
            path="/api/data",
            method="POST",
            content_types=[
                "application/json",
                "application/xml",
                "text/csv",
            ],
        ),
    ],
)

```

### Size Limits by Path

```python
app.add_middleware(
    RequestValidatorMiddleware,
    rules=[
        ValidationRule(
            path="/api/json",
            method="POST",
            max_body_size=1 * 1024 * 1024,  # 1 MB
        ),
        ValidationRule(
            path="/api/upload",
            method="POST",
            max_body_size=100 * 1024 * 1024,  # 100 MB
        ),
    ],
)

```

### Webhook Validation

```python
app.add_middleware(
    RequestValidatorMiddleware,
    rules=[
        ValidationRule(
            path="/webhooks/*",
            method="POST",
            required_headers=["X-Webhook-Signature", "X-Webhook-Timestamp"],
            content_types=["application/json"],
        ),
    ],
)

```

## Error Response

```json
{
    "error": "Bad Request",
    "detail": "Missing required header: Authorization",
    "status_code": 400
}

```

```json
{
    "error": "Unsupported Media Type",
    "detail": "Content-Type 'text/plain' not allowed. Expected: application/json",
    "status_code": 415
}

```

## Related Middlewares

- [ContentTypeMiddleware](content-type.md) - Content-Type validation
- [PayloadSizeMiddleware](payload-size.md) - Size limits
- [JSONSchemaMiddleware](json-schema.md) - JSON Schema validation
