# EarlyHintsMiddleware

HTTP 103 Early Hints for preloading resources.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import EarlyHintsMiddleware, EarlyHint

app = FastAPI()

app.add_middleware(
    EarlyHintsMiddleware,
    global_hints=[
        EarlyHint("/static/css/main.css", as_type="style"),
        EarlyHint("/static/js/app.js", as_type="script"),
    ],
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `global_hints` | `list[EarlyHint]` | `[]` | Hints for all requests |
| `path_hints` | `dict[str, list[EarlyHint]]` | `{}` | Path-specific hints |

## EarlyHint Fields

| Field | Type | Description |
| ------- | ------ | ------------- |
| `href` | `str` | Resource URL |
| `as_type` | `str` | Resource type (style, script, font, image) |
| `crossorigin` | `str` | Crossorigin attribute |
| `rel` | `str` | Link relation (default: preload) |

## How It Works

1. Middleware sends `Link` header with preload hints
2. Browser can start fetching resources before main response
3. Page loads faster as critical resources are preloaded

## Examples

### Global Preload Hints

```python
app.add_middleware(
    EarlyHintsMiddleware,
    global_hints=[
        EarlyHint("/static/css/main.css", as_type="style"),
        EarlyHint("/static/js/app.js", as_type="script"),
        EarlyHint("/static/fonts/inter.woff2", as_type="font", crossorigin="anonymous"),
    ],
)

```

### Path-Specific Hints

```python
app.add_middleware(
    EarlyHintsMiddleware,
    global_hints=[
        EarlyHint("/static/css/main.css", as_type="style"),
    ],
    path_hints={
        "/dashboard": [
            EarlyHint("/static/js/dashboard.js", as_type="script"),
            EarlyHint("/static/css/dashboard.css", as_type="style"),
        ],
        "/checkout": [
            EarlyHint("/static/js/checkout.js", as_type="script"),
            EarlyHint("/api/cart", rel="preconnect"),
        ],
    },
)

```

### Preconnect to External Services

```python
app.add_middleware(
    EarlyHintsMiddleware,
    global_hints=[
        EarlyHint("https://fonts.googleapis.com", rel="preconnect"),
        EarlyHint("https://cdn.example.com", rel="preconnect"),
        EarlyHint("https://api.stripe.com", rel="preconnect"),
    ],
)

```

### Font Preloading

```python
app.add_middleware(
    EarlyHintsMiddleware,
    global_hints=[
        EarlyHint(
            "/fonts/roboto.woff2",
            as_type="font",
            crossorigin="anonymous",
        ),
        EarlyHint(
            "/fonts/icons.woff2",
            as_type="font",
            crossorigin="anonymous",
        ),
    ],
)

```

## Response Headers

```http
Link: </static/css/main.css>; rel=preload; as=style
Link: </static/js/app.js>; rel=preload; as=script
Link: </fonts/inter.woff2>; rel=preload; as=font; crossorigin

```

## Browser Support

Early Hints (HTTP 103) is supported in:

- Chrome 103+

- Edge 103+

- Firefox (behind flag)

For unsupported browsers, Link headers are still sent and can be used.

## Related Middlewares

- [CompressionMiddleware](compression.md) - Response compression
- [CacheMiddleware](cache.md) - HTTP caching
