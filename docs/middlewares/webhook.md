# WebhookMiddleware

Validate incoming webhook signatures.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import WebhookMiddleware

app = FastAPI()

app.add_middleware(
    WebhookMiddleware,
    secret_key="webhook-secret",
    signature_header="X-Webhook-Signature",
    paths={"/webhooks/stripe", "/webhooks/github"},
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `secret_key` | `str` | Required | Webhook secret |
| `signature_header` | `str` | `"X-Webhook-Signature"` | Signature header |
| `paths` | `set[str]` | `set()` | Paths to validate |
| `algorithm` | `str` | `"sha256"` | Hash algorithm |

## Examples

### Single Webhook Endpoint

```python
app.add_middleware(
    WebhookMiddleware,
    secret_key="whsec_abc123",
    paths={"/webhooks/stripe"},
)

```

### Multiple Endpoints

```python
app.add_middleware(
    WebhookMiddleware,
    secret_key="my-secret",
    paths={
        "/webhooks/stripe",
        "/webhooks/github",
        "/webhooks/twilio",
    },
)

```

### Stripe Webhooks

```python
app.add_middleware(
    WebhookMiddleware,
    secret_key=os.getenv("STRIPE_WEBHOOK_SECRET"),
    signature_header="Stripe-Signature",
    paths={"/webhooks/stripe"},
)

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.json()
    event_type = payload["type"]

    if event_type == "payment_intent.succeeded":
        await handle_payment(payload["data"]["object"])

    return {"received": True}

```

### GitHub Webhooks

```python
app.add_middleware(
    WebhookMiddleware,
    secret_key=os.getenv("GITHUB_WEBHOOK_SECRET"),
    signature_header="X-Hub-Signature-256",
    paths={"/webhooks/github"},
)

@app.post("/webhooks/github")
async def github_webhook(request: Request):
    event = request.headers.get("X-GitHub-Event")
    payload = await request.json()

    if event == "push":
        await handle_push(payload)
    elif event == "pull_request":
        await handle_pr(payload)

    return {"ok": True}

```

### Multiple Providers

```python
from fastmiddleware import WebhookMiddleware

# Stripe
stripe_webhook = WebhookMiddleware(
    app,
    secret_key=os.getenv("STRIPE_SECRET"),
    signature_header="Stripe-Signature",
    paths={"/webhooks/stripe"},
)

# GitHub (add as another middleware)
github_webhook = WebhookMiddleware(
    stripe_webhook,  # Chain middlewares
    secret_key=os.getenv("GITHUB_SECRET"),
    signature_header="X-Hub-Signature-256",
    paths={"/webhooks/github"},
)

```

### Custom Signature Format

```python
from fastmiddleware import WebhookMiddleware

class CustomWebhook(WebhookMiddleware):
    def parse_signature(self, header: str) -> str:
        # Custom format: "sha256=abc123"
        if "=" in header:
            return header.split("=", 1)[1]
        return header

app.add_middleware(CustomWebhook, secret_key="...", paths={"/webhooks/custom"})

```

## Signature Verification

Standard format:

```http
X-Webhook-Signature: sha256=abc123def456...

```

Calculation:

```text
HMAC-SHA256(secret, request_body)

```

## Error Response

```json
{
    "error": "Unauthorized",
    "detail": "Invalid webhook signature",
    "status_code": 401
}

```

## Related Middlewares

- [RequestSigningMiddleware](request-signing.md) - HMAC validation
- [ReplayPreventionMiddleware](replay-prevention.md) - Prevent replays
- [IPFilterMiddleware](ip-filter.md) - IP filtering
