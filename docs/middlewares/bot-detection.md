# BotDetectionMiddleware

Detect and handle bot traffic based on User-Agent and behavior patterns.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import BotDetectionMiddleware, BotAction

app = FastAPI()

app.add_middleware(
    BotDetectionMiddleware,
    action=BotAction.TAG,
    block_malicious=True,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `action` | `BotAction` | `TAG` | Action for detected bots |
| `block_malicious` | `bool` | `True` | Block known malicious bots |
| `allow_good_bots` | `set[str]` | `{"googlebot", "bingbot"}` | Allowed good bots |
| `custom_patterns` | `list[str]` | `[]` | Custom bot detection patterns |

## Bot Actions

| Action | Description |
| -------- | ------------- |
| `BotAction.TAG` | Tag request, allow through |
| `BotAction.BLOCK` | Block with 403 Forbidden |
| `BotAction.CHALLENGE` | Return challenge (captcha) |
| `BotAction.THROTTLE` | Apply stricter rate limits |

## Examples

### Tag Bots (Default)

```python
app.add_middleware(
    BotDetectionMiddleware,
    action=BotAction.TAG,
)

@app.get("/")
async def handler(request: Request):
    is_bot = getattr(request.state, "is_bot", False)
    bot_name = getattr(request.state, "bot_name", None)
    return {"is_bot": is_bot, "bot": bot_name}

```

### Block All Bots

```python
app.add_middleware(
    BotDetectionMiddleware,
    action=BotAction.BLOCK,
    allow_good_bots=set(),  # Block all bots
)

```

### Allow Search Engine Bots

```python
app.add_middleware(
    BotDetectionMiddleware,
    action=BotAction.BLOCK,
    allow_good_bots={"googlebot", "bingbot", "duckduckbot", "yandexbot"},
)

```

### Custom Bot Patterns

```python
app.add_middleware(
    BotDetectionMiddleware,
    action=BotAction.TAG,
    custom_patterns=[
        r"my-internal-bot",
        r"monitoring-service",
    ],
)

```

### Throttle Bots

```python
app.add_middleware(
    BotDetectionMiddleware,
    action=BotAction.THROTTLE,
)

# Bots get stricter rate limits applied

```

## Request State

After middleware processes the request:

```python
request.state.is_bot       # bool - Is this a bot?
request.state.bot_name     # str | None - Bot identifier
request.state.bot_category # str - "search", "social", "monitoring", "malicious"

```

## Detected Bot Categories

- **Search Engines**: Googlebot, Bingbot, DuckDuckBot, etc.
- **Social**: Facebook, Twitter, LinkedIn crawlers
- **Monitoring**: Pingdom, UptimeRobot, etc.
- **Malicious**: Scrapers, vulnerability scanners

## Related Middlewares

- [UserAgentMiddleware](user-agent.md) - Parse User-Agent details
- [RateLimitMiddleware](rate-limit.md) - Rate limiting
- [HoneypotMiddleware](honeypot.md) - Trap malicious requests
