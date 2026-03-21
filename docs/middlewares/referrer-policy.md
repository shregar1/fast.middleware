# ReferrerPolicyMiddleware

Set Referrer-Policy header for privacy control.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ReferrerPolicyMiddleware

app = FastAPI()

app.add_middleware(
    ReferrerPolicyMiddleware,
    policy="strict-origin-when-cross-origin",
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `policy` | `str` | `"strict-origin-when-cross-origin"` | Referrer policy |

## Policy Options

| Policy | Description |
| -------- | ------------- |
| `no-referrer` | Never send referrer |
| `no-referrer-when-downgrade` | No referrer on HTTPS→HTTP |
| `origin` | Send only origin |
| `origin-when-cross-origin` | Full URL same-origin, origin cross-origin |
| `same-origin` | Only send for same-origin |
| `strict-origin` | Origin only, no downgrade |
| `strict-origin-when-cross-origin` | Full same-origin, origin cross-origin, no downgrade |
| `unsafe-url` | Always send full URL (not recommended) |

## Examples

### Strict Policy (Recommended)

```python
app.add_middleware(
    ReferrerPolicyMiddleware,
    policy="strict-origin-when-cross-origin",
)

```

### No Referrer (Maximum Privacy)

```python
app.add_middleware(
    ReferrerPolicyMiddleware,
    policy="no-referrer",
)

```

### Same Origin Only

```python
app.add_middleware(
    ReferrerPolicyMiddleware,
    policy="same-origin",
)

```

### Origin Only

```python
app.add_middleware(
    ReferrerPolicyMiddleware,
    policy="origin",
)

# https://example.com/page?secret=123

# Sends: https://example.com (path stripped)

```

## Policy Comparison

| Scenario | no-referrer | origin | strict-origin-when-cross-origin |
| ---------- | ------------- | -------- | -------------------------------- |
| Same origin | None | Origin | Full URL |
| Cross origin HTTPS→HTTPS | None | Origin | Origin |
| Cross origin HTTPS→HTTP | None | Origin | None |

## Response Header

```http
Referrer-Policy: strict-origin-when-cross-origin

```

## Use Cases

1. **Privacy** - Prevent leaking URLs to third parties
2. **Security** - Protect sensitive URL parameters
3. **Compliance** - GDPR, privacy regulations

## Related Middlewares

- [SecurityHeadersMiddleware](security-headers.md) - All security headers
- [PermissionsPolicyMiddleware](permissions-policy.md) - Feature permissions
