# UserAgentMiddleware

User-Agent parsing and device detection middleware.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import UserAgentMiddleware, UserAgentConfig, get_user_agent

app = FastAPI()

# Basic usage
app.add_middleware(UserAgentMiddleware)

# With config
config = UserAgentConfig(
    add_headers=True,       # Add X-Device-Type, X-Browser headers
    cache_results=True,     # Cache parsed results
)
app.add_middleware(UserAgentMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `add_headers` | `bool` | `False` | Add device info headers |
| `cache_results` | `bool` | `True` | Cache parsed UA strings |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## Getting User Agent Info

```python
from fastmiddleware import get_user_agent

@app.get("/")
async def handler():
    ua = get_user_agent()

    return {
        "browser": ua["browser"],
        "browser_version": ua["browser_version"],
        "os": ua["os"],
        "os_version": ua["os_version"],
        "device": ua["device"],
        "is_mobile": ua["is_mobile"],
        "is_tablet": ua["is_tablet"],
        "is_desktop": ua["is_desktop"],
        "is_bot": ua["is_bot"],
    }

```

## Parsed Information

| Field | Type | Example Values |
| ------- | ------ | ---------------- |
| `browser` | `str` | Chrome, Firefox, Safari, Edge |
| `browser_version` | `str` | 120.0.0 |
| `os` | `str` | Windows, macOS, iOS, Android, Linux |
| `os_version` | `str` | 10.0, 14.2 |
| `device` | `str` | Desktop, Mobile, Tablet, Bot |
| `is_mobile` | `bool` | True/False |
| `is_tablet` | `bool` | True/False |
| `is_desktop` | `bool` | True/False |
| `is_bot` | `bool` | True/False |

## Adaptive Responses

```python
@app.get("/page")
async def page():
    ua = get_user_agent()

    if ua["is_mobile"]:
        return mobile_response()
    elif ua["is_tablet"]:
        return tablet_response()
    else:
        return desktop_response()

@app.get("/api/data")
async def data():
    ua = get_user_agent()

    if ua["is_bot"]:
        # Return minimal data for bots
        return {"title": "Page Title"}

    return full_response()

```

## Response Headers (if enabled)

| Header | Value |
| -------- | ------- |
| `X-Device-Type` | Desktop, Mobile, Tablet, Bot |
| `X-Browser` | Chrome, Firefox, Safari, etc. |

## Request State Access

```python
@app.get("/")
async def handler(request: Request):
    ua_info = request.state.user_agent
    return {"browser": ua_info.browser}

```

## Related Middlewares

- [BotDetectionMiddleware](bot-detection.md)
- [ClientHintsMiddleware](client-hints.md)
- [RequestFingerprintMiddleware](request-fingerprint.md)
