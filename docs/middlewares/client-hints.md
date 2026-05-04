# ClientHintsMiddleware

Support for HTTP Client Hints for adaptive content delivery.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ClientHintsMiddleware, get_client_hints

app = FastAPI()

app.add_middleware(
    ClientHintsMiddleware,
    request_hints=["DPR", "Viewport-Width", "Save-Data"],
)

@app.get("/")
async def handler():
    hints = get_client_hints()
    return hints

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `request_hints` | `list[str]` | `[]` | Hints to request from browser |
| `critical_hints` | `list[str]` | `[]` | Critical hints (blocking) |

## Available Client Hints

| Hint | Description |
| ------ | ------------- |
| `DPR` | Device pixel ratio |
| `Viewport-Width` | Viewport width in pixels |
| `Width` | Resource width |
| `Save-Data` | User prefers reduced data |
| `Sec-CH-UA` | User agent brand |
| `Sec-CH-UA-Mobile` | Is mobile device |
| `Sec-CH-UA-Platform` | Operating system |

## Helper Functions

### `get_client_hints() -> dict`

Returns parsed client hints for the current request.

```python
from fastmiddleware import get_client_hints

@app.get("/image")
async def get_image():
    hints = get_client_hints()

    dpr = hints.get("dpr", 1)
    save_data = hints.get("save_data", False)

    if save_data:
        return serve_low_quality_image()
    elif dpr >= 2:
        return serve_retina_image()
    else:
        return serve_standard_image()

```

## Examples

### Basic Client Hints

```python
app.add_middleware(
    ClientHintsMiddleware,
    request_hints=["DPR", "Viewport-Width"],
)

# Response includes:

# Accept-CH: DPR, Viewport-Width

```

### With Save-Data Detection

```python
app.add_middleware(
    ClientHintsMiddleware,
    request_hints=["Save-Data", "DPR"],
)

@app.get("/content")
async def content():
    hints = get_client_hints()

    if hints.get("save_data"):
        return {"content": "Lightweight version"}
    return {"content": "Full version with images"}

```

### Adaptive Image Serving

```python
from fastmiddleware import ClientHintsMiddleware, get_client_hints

app.add_middleware(
    ClientHintsMiddleware,
    request_hints=["DPR", "Width", "Viewport-Width"],
)

@app.get("/images/{image_id}")
async def get_image(image_id: str):
    hints = get_client_hints()

    dpr = hints.get("dpr", 1)
    width = hints.get("width", 800)

    # Calculate optimal image size
    optimal_width = int(width * dpr)

    return serve_resized_image(image_id, optimal_width)

```

### Critical Hints

```python
app.add_middleware(
    ClientHintsMiddleware,
    request_hints=["DPR", "Viewport-Width"],
    critical_hints=["DPR"],  # Browser must send on first request
)

```

## Response Headers

```http
Accept-CH: DPR, Viewport-Width, Save-Data
Accept-CH-Lifetime: 86400
Critical-CH: DPR

```

## Related Middlewares

- [UserAgentMiddleware](user-agent.md) - Parse User-Agent
- [ContentNegotiationMiddleware](content-negotiation.md) - Content type negotiation
- [CompressionMiddleware](compression.md) - Response compression
