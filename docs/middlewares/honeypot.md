# HoneypotMiddleware

Honeypot trap middleware for detecting attackers.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import HoneypotMiddleware, HoneypotConfig

app = FastAPI()

# Basic usage
app.add_middleware(
    HoneypotMiddleware,
    honeypot_paths={"/admin.php", "/wp-admin", "/.env"},
)

# With config
config = HoneypotConfig(
    honeypot_paths={
        "/admin.php",
        "/wp-admin",
        "/wp-login.php",
        "/.env",
        "/.git/config",
        "/config.php",
        "/phpinfo.php",
        "/backup.sql",
    },
    block_on_access=True,
    block_duration=3600,  # 1 hour
    log_access=True,
    fake_delay=2.0,  # Waste attacker time
)
app.add_middleware(HoneypotMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `honeypot_paths` | `Set[str]` | See below | Trap endpoints |
| `block_on_access` | `bool` | `True` | Block IPs that access |
| `block_duration` | `int` | `3600` | Block duration in seconds |
| `log_access` | `bool` | `True` | Log honeypot access |
| `fake_delay` | `float` | `2.0` | Response delay (wastes time) |
| `logger_name` | `str` | `"honeypot"` | Logger name |

## Default Honeypot Paths

```python
{
    "/admin.php",
    "/wp-admin",
    "/wp-login.php",
    "/.env",
    "/config.php",
    "/phpinfo.php",
    "/.git/config",
    "/backup.sql",
    "/db.sql",
    "/api/v1/admin/debug",
}

```

## How It Works

1. **Trap Detection**: Request matches honeypot path
2. **Logging**: Log attacker IP, path, user agent
3. **Delay**: Add fake delay to waste attacker time
4. **Block**: Optionally block IP for future requests
5. **Response**: Return 404 (looks like normal not found)

## Access Log Format

```text
WARNING: Honeypot accessed: /.env from 192.168.1.100

```

## Getting Access Logs

```python
honeypot = HoneypotMiddleware(app, honeypot_paths={...})

# Get access log
access_log = honeypot._access_log

# [{"timestamp": 1704067200, "ip": "192.168.1.100", "path": "/.env", ...}]

```

## Blocked IPs

After accessing a honeypot, the IP receives 403 on all requests:

```json
{
  "error": true,
  "message": "Access denied"
}

```

## Best Practices

1. Use paths that attackers commonly probe
2. Keep honeypot paths secret from your team
3. Monitor honeypot logs for attack patterns
4. Consider integrating with fail2ban or similar

## Related Middlewares

- [IPFilterMiddleware](ip-filter.md) - IP blocking
- [BotDetectionMiddleware](bot-detection.md)
- [RateLimitMiddleware](rate-limit.md)
