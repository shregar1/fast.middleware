---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## Middleware Affected

- [ ] CORSMiddleware
- [ ] SecurityHeadersMiddleware
- [ ] RateLimitMiddleware
- [ ] AuthenticationMiddleware
- [ ] Other: _______________

## To Reproduce

Steps to reproduce the behavior:

1. Configure middleware with '...'
2. Send request to '...'
3. See error

## Expected Behavior

A clear description of what you expected to happen.

## Actual Behavior

What actually happened.

## Code Example

```python
from fastmiddleware import ...

app.add_middleware(...)

```

## Error Message / Traceback

```text
Paste error message here

```

## Environment

- OS: [e.g., Ubuntu 22.04, macOS 14.0]
- Python version: [e.g., 3.11.5]
- FastAPI version: [e.g., 0.109.0]
- fast-middleware version: [e.g., 0.5.0]

## Additional Context

Add any other context about the problem here.
