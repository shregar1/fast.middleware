# PermissionsPolicyMiddleware

Control browser feature permissions via Permissions-Policy header.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import PermissionsPolicyMiddleware

app = FastAPI()

app.add_middleware(
    PermissionsPolicyMiddleware,
    policies={
        "camera": [],
        "microphone": [],
        "geolocation": ["self"],
    },
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `policies` | `dict[str, list[str]]` | `{}` | Feature policies |

## Policy Values

| Value | Meaning |
| ------- | --------- |
| `[]` | Disabled for all |
| `["self"]` | Allowed for same origin |
| `["*"]` | Allowed for all |
| `["https://example.com"]` | Allowed for specific origin |

## Available Features

| Feature | Description |
| --------- | ------------- |
| `camera` | Camera access |
| `microphone` | Microphone access |
| `geolocation` | Geolocation API |
| `fullscreen` | Fullscreen API |
| `payment` | Payment Request API |
| `usb` | WebUSB API |
| `accelerometer` | Accelerometer sensor |
| `gyroscope` | Gyroscope sensor |
| `autoplay` | Media autoplay |

## Examples

### Disable All Features

```python
app.add_middleware(
    PermissionsPolicyMiddleware,
    policies={
        "camera": [],
        "microphone": [],
        "geolocation": [],
        "fullscreen": [],
        "payment": [],
        "usb": [],
    },
)

```

### Allow for Same Origin

```python
app.add_middleware(
    PermissionsPolicyMiddleware,
    policies={
        "camera": ["self"],
        "microphone": ["self"],
        "geolocation": ["self"],
        "fullscreen": ["self"],
    },
)

```

### Specific Origins

```python
app.add_middleware(
    PermissionsPolicyMiddleware,
    policies={
        "fullscreen": ["self", "https://youtube.com"],
        "payment": ["self", "https://stripe.com"],
    },
)

```

### Video Conferencing App

```python
app.add_middleware(
    PermissionsPolicyMiddleware,
    policies={
        "camera": ["self"],
        "microphone": ["self"],
        "fullscreen": ["self"],
        "display-capture": ["self"],
        "geolocation": [],  # Not needed
        "payment": [],
    },
)

```

### E-commerce Site

```python
app.add_middleware(
    PermissionsPolicyMiddleware,
    policies={
        "payment": ["self", "https://pay.google.com", "https://www.paypal.com"],
        "geolocation": ["self"],  # For store locator
        "camera": [],
        "microphone": [],
    },
)

```

## Response Header

```http
Permissions-Policy: camera=(), microphone=(), geolocation=(self)

```

## Browser Support

Modern browsers support Permissions-Policy. Older browsers may use Feature-Policy (deprecated).

## Related Middlewares

- [SecurityHeadersMiddleware](security-headers.md) - All security headers
- [ReferrerPolicyMiddleware](referrer-policy.md) - Referrer policy
- [CSPReportMiddleware](csp-report.md) - CSP reporting
