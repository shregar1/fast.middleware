# IPFilterMiddleware

IP-based access control with whitelist and blacklist support.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import IPFilterMiddleware, IPFilterConfig

app = FastAPI()

# Whitelist mode - only allow these IPs
app.add_middleware(
    IPFilterMiddleware,
    whitelist={"192.168.1.0/24", "10.0.0.0/8"},
)

# Blacklist mode - block these IPs
app.add_middleware(
    IPFilterMiddleware,
    blacklist={"192.168.1.100", "10.0.0.50"},
)

# With config
config = IPFilterConfig(
    whitelist={"192.168.1.0/24"},
    blacklist={"192.168.1.100"},  # Blacklist takes precedence
    block_private=False,
    trust_proxy=True,
)
app.add_middleware(IPFilterMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `whitelist` | `Set[str]` | `set()` | Allowed IPs/CIDRs (if set, only these allowed) |
| `blacklist` | `Set[str]` | `set()` | Blocked IPs/CIDRs |
| `block_private` | `bool` | `False` | Block private IP ranges |
| `trust_proxy` | `bool` | `True` | Trust X-Forwarded-For header |
| `exclude_paths` | `Set[str]` | `set()` | Paths to skip filtering |

## CIDR Support

Supports both individual IPs and CIDR notation:

```python
whitelist={
    "192.168.1.100",      # Single IP
    "192.168.1.0/24",     # 256 IPs
    "10.0.0.0/8",         # Class A network
    "2001:db8::/32",      # IPv6 range
}

```

## Response Codes

| Code | Description |
| ------ | ------------- |
| 403 | IP not in whitelist or in blacklist |

## Related Middlewares

- [RateLimitMiddleware](rate-limit.md) - Rate limit by IP
- [RealIPMiddleware](real-ip.md) - Get real client IP
