# ContentNegotiationMiddleware

Negotiate response content type based on Accept header.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ContentNegotiationMiddleware, get_negotiated_type

app = FastAPI()

app.add_middleware(
    ContentNegotiationMiddleware,
    supported_types=["application/json", "application/xml", "text/html"],
)

@app.get("/")
async def handler():
    content_type = get_negotiated_type()
    return {"negotiated": content_type}

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `supported_types` | `list[str]` | `["application/json"]` | Content types you support |
| `default_type` | `str` | `"application/json"` | Default when no match |
| `strict` | `bool` | `False` | Return 406 if no match |

## Helper Functions

### `get_negotiated_type() -> str`

Returns the negotiated content type for the current request.

```python
from fastmiddleware import get_negotiated_type

@app.get("/users")
async def get_users():
    content_type = get_negotiated_type()

    users = await db.get_users()

    if content_type == "application/xml":
        return Response(
            content=users_to_xml(users),
            media_type="application/xml"
        )
    elif content_type == "text/html":
        return Response(
            content=render_html(users),
            media_type="text/html"
        )
    else:
        return users  # JSON by default

```

## Examples

### Basic Content Negotiation

```python
app.add_middleware(
    ContentNegotiationMiddleware,
    supported_types=["application/json", "application/xml"],
)

# Request: Accept: application/xml

# get_negotiated_type() returns: "application/xml"

```

### Strict Mode (406 on No Match)

```python
app.add_middleware(
    ContentNegotiationMiddleware,
    supported_types=["application/json"],
    strict=True,
)

# Request: Accept: text/plain

# Response: 406 Not Acceptable

```

### Multiple Format Support

```python
from fastapi import Response
from fastmiddleware import ContentNegotiationMiddleware, get_negotiated_type

app.add_middleware(
    ContentNegotiationMiddleware,
    supported_types=[
        "application/json",
        "application/xml",
        "text/csv",
        "text/html",
    ],
)

@app.get("/data")
async def get_data():
    data = await fetch_data()
    content_type = get_negotiated_type()

    formatters = {
        "application/json": lambda d: JSONResponse(d),
        "application/xml": lambda d: Response(to_xml(d), media_type="application/xml"),
        "text/csv": lambda d: Response(to_csv(d), media_type="text/csv"),
        "text/html": lambda d: HTMLResponse(render(d)),
    }

    formatter = formatters.get(content_type, formatters["application/json"])
    return formatter(data)

```

### With Quality Weights

```python

# Request: Accept: application/xml;q=0.9, application/json;q=1.0

# Result: "application/json" (higher quality weight)

```

## Request State

```python
request.state.negotiated_type  # The selected content type
request.state.accept_types     # Parsed Accept header

```

## Related Middlewares

- [AcceptLanguageMiddleware](accept-language.md) - Language negotiation
- [ResponseFormatMiddleware](response-format.md) - Response formatting
- [CompressionMiddleware](compression.md) - Response compression
