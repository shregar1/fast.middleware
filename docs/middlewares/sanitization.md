# SanitizationMiddleware

Sanitize input to prevent XSS and injection attacks.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import SanitizationMiddleware

app = FastAPI()

app.add_middleware(
    SanitizationMiddleware,
    escape_html=True,
    strip_tags=True,
    remove_null_bytes=True,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `escape_html` | `bool` | `True` | Escape HTML entities |
| `strip_tags` | `bool` | `False` | Remove HTML tags |
| `remove_null_bytes` | `bool` | `True` | Remove null bytes |
| `trim_whitespace` | `bool` | `True` | Trim leading/trailing |
| `max_length` | `int` | `None` | Truncate long strings |

## Examples

### Basic Sanitization

```python
app.add_middleware(
    SanitizationMiddleware,
    escape_html=True,
    remove_null_bytes=True,
)

# Input: {"name": "<script>alert('xss')</script>"}

# Sanitized: {"name": "&lt;script&gt;alert('xss')&lt;/script&gt;"}

```

### Strip HTML Tags

```python
app.add_middleware(
    SanitizationMiddleware,
    strip_tags=True,
)

# Input: {"name": "<b>John</b> <script>evil()</script>"}

# Sanitized: {"name": "John"}

```

### Remove Null Bytes

```python
app.add_middleware(
    SanitizationMiddleware,
    remove_null_bytes=True,
)

# Input: {"name": "John\x00Doe"}

# Sanitized: {"name": "JohnDoe"}

```

### Truncate Long Strings

```python
app.add_middleware(
    SanitizationMiddleware,
    max_length=1000,
)

# Long strings are truncated to 1000 characters

```

### Combine Options

```python
app.add_middleware(
    SanitizationMiddleware,
    escape_html=True,
    strip_tags=False,
    remove_null_bytes=True,
    trim_whitespace=True,
    max_length=5000,
)

```

### Exclude Paths

```python
from fastmiddleware import SanitizationMiddleware, SanitizationConfig

config = SanitizationConfig(
    escape_html=True,
    exclude_paths={"/api/html-content", "/api/rich-text"},
)

app.add_middleware(SanitizationMiddleware, config=config)

```

### Sanitize Specific Fields

```python
from fastmiddleware import SanitizationMiddleware

class SelectiveSanitization(SanitizationMiddleware):
    sanitize_fields = {"name", "description", "comment", "bio"}

    def should_sanitize_field(self, field_name: str) -> bool:
        return field_name in self.sanitize_fields

app.add_middleware(SelectiveSanitization, escape_html=True)

```

## Sanitization Rules

| Input | escape_html | strip_tags |
| ------- | ------------- | ------------ |
| `<script>` | `&lt;script&gt;` | (removed) |
| `<b>text</b>` | `&lt;b&gt;text&lt;/b&gt;` | `text` |
| `"quotes"` | `&quot;quotes&quot;` | `"quotes"` |

## Use Cases

1. **XSS Prevention** - Escape user input before display
2. **SQL Injection** - Remove null bytes and special chars
3. **Data Cleaning** - Normalize input data
4. **Security Hardening** - Defense in depth

## Related Middlewares

- [DataMaskingMiddleware](data-masking.md) - Mask sensitive data
- [RequestValidatorMiddleware](request-validator.md) - Request validation
- [ContentTypeMiddleware](content-type.md) - Content-Type validation
