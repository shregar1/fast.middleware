# DataMaskingMiddleware

Mask sensitive data in logs and responses.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import DataMaskingMiddleware, MaskingRule

app = FastAPI()

app.add_middleware(
    DataMaskingMiddleware,
    rules=[
        MaskingRule(field="password", mask="***"),
        MaskingRule(field="ssn", mask="XXX-XX-****"),
        MaskingRule(field="credit_card", mask="****-****-****-{last4}"),
    ],
)

```

## Configuration

|Parameter|Type|Default|Description|
| ----------- | ------ | --------- | ------------- |
|`rules`|`list[MaskingRule]`|`[]`|Masking rules to apply|
|`mask_in_logs`|`bool`|`True`|Mask in log output|
|`mask_in_response`|`bool`|`False`|Mask in responses|

## MaskingRule Options

|Field|Type|Description|
| ------- | ------ | ------------- |
|`field`|`str`|Field name to mask|
|`mask`|`str`|Mask pattern|
|`pattern`|`str`|Regex pattern for value matching|

## Examples

### Basic Field Masking

```python
app.add_middleware(
    DataMaskingMiddleware,
    rules=[
        MaskingRule(field="password", mask="[REDACTED]"),
        MaskingRule(field="api_key", mask="***"),
    ],
)

# Input: {"password": "secret123", "username": "john"}

# Logged: {"password": "[REDACTED]", "username": "john"}

```

### Partial Masking

```python
app.add_middleware(
    DataMaskingMiddleware,
    rules=[
        MaskingRule(field="email", mask="{first3}***@{domain}"),
        MaskingRule(field="phone", mask="***-***-{last4}"),
        MaskingRule(field="ssn", mask="XXX-XX-{last4}"),
    ],
)

# email: "john@example.com" -> "joh***@example.com"

# phone: "555-123-4567" -> "***-***-4567"

# ssn: "123-45-6789" -> "XXX-XX-6789"

```

### Credit Card Masking

```python
app.add_middleware(
    DataMaskingMiddleware,
    rules=[
        MaskingRule(
            field="card_number",
            mask="****-****-****-{last4}",
        ),
        MaskingRule(field="cvv", mask="***"),
    ],
)

# card_number: "4111-1111-1111-1234" -> "****-****-****-1234"

```

### Regex Pattern Matching

```python
app.add_middleware(
    DataMaskingMiddleware,
    rules=[
        MaskingRule(
            field="*",  # Any field
            pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            mask="[EMAIL]",
        ),
        MaskingRule(
            field="*",
            pattern=r"\b\d{3}-\d{2}-\d{4}\b",  # SSN pattern
            mask="[SSN]",
        ),
    ],
)

```

### Mask in Responses

```python
app.add_middleware(
    DataMaskingMiddleware,
    mask_in_response=True,
    rules=[
        MaskingRule(field="internal_id", mask="[HIDDEN]"),
    ],
)

# Response body is also masked before sending

```

### Nested Field Masking

```python
app.add_middleware(
    DataMaskingMiddleware,
    rules=[
        MaskingRule(field="user.password", mask="***"),
        MaskingRule(field="payment.card.number", mask="****"),
    ],
)

# {"user": {"password": "xxx"}} -> {"user": {"password": "***"}}

```

## Use Cases

1. **GDPR Compliance** - Mask PII in logs
2. **PCI DSS** - Mask credit card data
3. **HIPAA** - Mask healthcare information
4. **Security** - Prevent sensitive data exposure

## Related Middlewares

- [AuditMiddleware](audit.md) - Audit logging
- [LoggingMiddleware](logging.md) - Request logging
- [SanitizationMiddleware](sanitization.md) - Input sanitization
