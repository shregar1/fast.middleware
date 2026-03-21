# fastmvc_middleware

**HTTP middleware for FastAPI / Starlette** in the FastMVC monorepo: request correlation IDs (via `fastmvc_core`), optional security headers, response timing, CORS presets, body-size limits, client IP extraction, and gzip compression presets. This package is **not** the same as **`fastmvc_tenancy`** (tenant resolution) or **`fastmvc_core`** (configuration DTOs); it focuses on **cross-cutting ASGI behavior** you mount on your FastAPI app.

The `tests/` directory also contains legacy suites that target an optional **`fastmiddleware`** package (not installed by default). The default pytest configuration only runs the lightweight **`fastmvc_middleware`** tests—see `python_files` in [pyproject.toml](pyproject.toml).

## Layout

- `src/fastmvc_middleware/` — `RequestIDMiddleware`, `SecurityHeadersMiddleware`, `ResponseTimingMiddleware`, `CORSPreset`, `BodySizeLimitMiddleware`, `get_client_ip` / `ClientIPMiddleware`, `CompressionPreset`, and related helpers.

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

### CORS preset (SPA)

```python
from starlette.middleware.cors import CORSMiddleware
from fastmvc_middleware import CORSPreset

preset = CORSPreset(allow_origins=["https://app.example.com"], allow_credentials=True)
app.add_middleware(CORSMiddleware, **preset.starlette_kwargs())
```

### Body size limit (DoS guard)

Checks `Content-Length` before the handler runs; use a reverse-proxy limit for chunked uploads without `Content-Length`.

```python
from fastmvc_middleware import BodySizeLimitMiddleware

app.add_middleware(BodySizeLimitMiddleware, max_bytes=512_000)
```

### Client IP (proxies)

```python
from fastmvc_middleware import ClientIPMiddleware, get_client_ip, read_client_ip

app.add_middleware(ClientIPMiddleware, trusted_proxy_depth=1)

@app.get("/who")
async def who(request):
    return {"ip": read_client_ip(request) or get_client_ip(request)}
```

Set `trusted_proxy_depth=0` to ignore `X-Forwarded-For` when the app is not behind a trusted proxy.

### Compression (gzip)

Starlette ships `GZipMiddleware` only (no brotli). Use a CDN or server-level brotli if needed.

```python
from fastmvc_middleware import CompressionPreset

CompressionPreset(minimum_size=500).add_to_app(app)
```

## Related packages

- **`fastmvc_tenancy`** — `TenantMiddleware` and tenant context (different concern).
- **`fastmvc_core`** — app config; not HTTP middleware.
- Monorepo: [../README.md](../README.md).

## Tooling

If this folder includes [CONTRIBUTING.md](CONTRIBUTING.md), [Makefile](Makefile), and [PUBLISHING.md](PUBLISHING.md) (synced from tooling scripts), use them for tests and lint.

---

## Documentation

| Document | Purpose |
|----------|---------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Dev setup, tests, monorepo sync |
| [PUBLISHING.md](PUBLISHING.md) | PyPI and releases |
| [SECURITY.md](SECURITY.md) | Reporting vulnerabilities |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

**Monorepo:** [../README.md](../README.md) · **Coverage:** [../docs/COVERAGE.md](../docs/COVERAGE.md)
