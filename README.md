# fastmvc_middleware

**HTTP middleware utilities** for FastMVC / Starlette applications.

---

## Overview

Cross-cutting concerns live here when they are **shared across many services** but do not belong in `fastmvc_tenancy` (tenant context) or `fastmvc_core` (config-only). Examples might include request ID injection, security headers, or custom logging — **subject to what is actually implemented in this folder**.

Install when your scaffold or product depends on it:

```bash
python -m pip install -e ./fastmvc_middleware
```

---

## Related packages

- **`fastmvc_tenancy`** — tenant resolution and JWT-related middleware patterns
- **`fastmvc_core`** — configuration, not WSGI/ASGI middleware

See [../README.md](../README.md).
