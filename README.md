# fastmvc_middleware

**HTTP middleware for FastAPI / Starlette** in the FastMVC monorepo: request correlation IDs (via `fastmvc_core`), optional security headers, and response timing. This package is **not** the same as **`fastmvc_tenancy`** (tenant resolution) or **`fastmvc_core`** (configuration DTOs); it focuses on **cross-cutting ASGI behavior** you mount on your FastAPI app.

The `tests/` directory also contains legacy suites that target an optional **`fastmiddleware`** package (not installed by default). The default pytest configuration only runs the lightweight **`fastmvc_middleware`** tests—see `python_files` in [pyproject.toml](pyproject.toml).

## Layout

- `src/fastmvc_middleware/` — `RequestIDMiddleware`, `SecurityHeadersMiddleware`, `ResponseTimingMiddleware`, and related helpers.

## Install

From the monorepo (if your project vendors this tree):

```bash
pip install -e ./fastmvc_middleware
```

## Usage

```python
from fastapi import FastAPI
from fastmvc_middleware import (
    RequestIDMiddleware,
    SecurityHeadersConfig,
    SecurityHeadersMiddleware,
    ResponseTimingMiddleware,
)

app = FastAPI()
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    SecurityHeadersMiddleware,
    config=SecurityHeadersConfig(
        hsts_max_age=31536000,
        hsts_include_subdomains=True,
        csp_frame_ancestors="'self'",
    ),
)
app.add_middleware(ResponseTimingMiddleware)  # X-Response-Time (seconds by default)
```

## Related packages

- **`fastmvc_tenancy`** — `TenantMiddleware` and tenant context (different concern).
- **`fastmvc_core`** — app config; not HTTP middleware.
- Monorepo: [../README.md](../README.md).

## Tooling

If this folder includes [CONTRIBUTING.md](CONTRIBUTING.md), [Makefile](Makefile), and [PUBLISHING.md](PUBLISHING.md) (synced from tooling scripts), use them for tests and lint.
