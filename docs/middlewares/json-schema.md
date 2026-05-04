# JSONSchemaMiddleware

JSON Schema validation middleware for request bodies.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import JSONSchemaMiddleware, JSONSchemaConfig

app = FastAPI()

# Define schemas
user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 100},
        "email": {"type": "string"},
        "age": {"type": "integer", "minimum": 0, "maximum": 150},
    },
    "required": ["name", "email"],
}

product_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "price": {"type": "number", "minimum": 0},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title", "price"],
}

# Apply middleware
app.add_middleware(
    JSONSchemaMiddleware,
    schemas={
        "/api/users": user_schema,
        "POST:/api/products": product_schema,  # Method-specific
    },
    strict=True,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `schemas` | `Dict[str, Dict]` | `{}` | Path to schema mapping |
| `strict` | `bool` | `True` | Return 400 on validation failure |

## Schema Matching

### Path Matching

```python
schemas={
    "/api/users": schema,        # All methods
    "/api/products/*": schema,   # Prefix match
}

```

### Method-Specific

```python
schemas={
    "POST:/api/users": create_schema,
    "PUT:/api/users": update_schema,
    "PATCH:/api/users": patch_schema,
}

```

## Supported Validations

| Validation | Types | Description |
| ------------ | ------- | ------------- |
| `type` | all | Type checking |
| `required` | object | Required fields |
| `properties` | object | Property schemas |
| `items` | array | Array item schema |
| `enum` | all | Allowed values |
| `minimum`/`maximum` | number | Number range |
| `minLength`/`maxLength` | string | String length |

## Validation Error Response

```json
{
  "error": true,
  "message": "Validation failed",
  "errors": [
    "Missing required field: email",
    "age: Value must be >= 0"
  ]
}

```

## Accessing Validated Data

```python
@app.post("/api/users")
async def create_user(request: Request):
    # Access validated body
    body = request.state.validated_body
    errors = request.state.validation_errors

    return {"user": body}

```

## Complex Schema Example

```python
order_schema = {
    "type": "object",
    "properties": {
        "customer": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
            },
            "required": ["name", "email"],
        },
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer"},
                    "quantity": {"type": "integer", "minimum": 1},
                },
                "required": ["product_id", "quantity"],
            },
        },
        "status": {"type": "string", "enum": ["pending", "confirmed", "shipped"]},
    },
    "required": ["customer", "items"],
}

```

## Related Middlewares

- [RequestValidatorMiddleware](request-validator.md)
- [ContentTypeMiddleware](content-type.md)
