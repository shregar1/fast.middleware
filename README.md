# fastx_middleware

**HTTP middleware for FastAPI / Starlette** in the FastMVC monorepo. The installable package is **`fastmiddleware`** (import `from fastmiddleware import …`); PyPI name is **`fastx-middleware`**. It ships **90+** ASGI middlewares—request correlation IDs (via `fastx_platform`), security headers, rate limiting, sessions, caching, i18n, routing helpers, **build/version headers**, **immutable static asset caching**, **DNS prefetch control**, and more. This package is **not** the same as **`fastx_tenancy`** (tenant resolution) or **`fastx_platform`** (configuration DTOs); it focuses on **cross-cutting ASGI behavior** you mount on your FastAPI app.

The `tests/` directory also contains legacy suites that target an optional **`fastmiddleware`** package (not installed by default). The default pytest configuration only runs the lightweight **`fastx_middleware`** tests—see `python_files` in [pyproject.toml](pyproject.toml).

## Layout

Source lives under **`src/`**, mapped to the **`fastmiddleware`** package (see `package-dir` in [pyproject.toml](pyproject.toml)):

| Section | Path | Role |
|--------|------|------|
| **mw_core** | `src/mw_core/` | Factory helpers, CORS, logging, timing, body limits, client IP, request ID, compression |
| **sec** | `src/sec/` | Security headers, CSRF, auth backends, JWT bearer, webhooks, trusted hosts, etc. |
| **operations** | `src/operations/` | Rate limits, metrics, health, sessions, caching, i18n, routing, **build/version**, **immutable static cache**, **DNS prefetch**, etc. |

See [src/taxonomy.py](src/taxonomy.py) for the section map.

## Install

From the monorepo (if your project vendors this tree):

```bash
pip install -e ./fastx_middleware
```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import (
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
from fastmiddleware import CORSPreset

preset = CORSPreset(allow_origins=["https://app.example.com"], allow_credentials=True)
app.add_middleware(CORSMiddleware, **preset.starlette_kwargs())
```

### Body size limit (DoS guard)

Checks `Content-Length` before the handler runs; use a reverse-proxy limit for chunked uploads without `Content-Length`.

```python
from fastmiddleware import BodySizeLimitMiddleware

app.add_middleware(BodySizeLimitMiddleware, max_bytes=512_000)
```

### Client IP (proxies)

```python
from fastmiddleware import ClientIPMiddleware, get_client_ip, read_client_ip

app.add_middleware(ClientIPMiddleware, trusted_proxy_depth=1)

@app.get("/who")
async def who(request):
    return {"ip": read_client_ip(request) or get_client_ip(request)}
```

Set `trusted_proxy_depth=0` to ignore `X-Forwarded-For` when the app is not behind a trusted proxy.

### Compression (gzip)

Starlette ships `GZipMiddleware` only (no brotli). Use a CDN or server-level brotli if needed.

```python
from fastmiddleware import CompressionPreset

CompressionPreset(minimum_size=500).add_to_app(app)
```

### Build / version headers (support & deploys)

Expose release metadata on every response (`APP_VERSION` and `GIT_SHA` by default):

```python
from fastmiddleware import BuildVersionMiddleware, BuildVersionConfig

app.add_middleware(
    BuildVersionMiddleware,
    config=BuildVersionConfig(
        version_header="X-App-Version",
        git_sha_header="X-Git-SHA",
    ),
)
```

### Immutable cache for static assets

Use with fingerprinted filenames (`app.[hash].js`). Adds `Cache-Control: public, max-age=…, immutable` for matching path prefixes.

```python
from fastmiddleware import ImmutableStaticCacheMiddleware, ImmutableStaticCacheConfig

app.add_middleware(
    ImmutableStaticCacheMiddleware,
    config=ImmutableStaticCacheConfig(
        path_prefixes=("/static/", "/assets/"),
        max_age_seconds=31_536_000,
    ),
)
```

### DNS prefetch control (privacy)

```python
from fastmiddleware import DNSPrefetchControlMiddleware

app.add_middleware(DNSPrefetchControlMiddleware)  # X-DNS-Prefetch-Control: off
```

### Edge performance tiers (CDN-class cache semantics)

Preset **Cache-Control** shapes for apps behind Cloudflare / Fastly / CloudFront—analogous to **feed (Instagram-class)**, **creator (subscription / mixed public–private)**, and **live (Twitch-class low-latency)** products. Sets `s-maxage`, **stale-while-revalidate**, optional **`CDN-Cache-Control`** and **`Surrogate-Control`**, plus **`Vary`**. Does not replace `Cache-Control` your handlers already set when `only_if_missing=True` (default).

```python
from fastmiddleware import (
    EdgePerformanceTier,
    EdgeTierCacheHeadersConfig,
    EdgeTierCacheHeadersMiddleware,
)

app.add_middleware(
    EdgeTierCacheHeadersMiddleware,
    config=EdgeTierCacheHeadersConfig(tier=EdgePerformanceTier.FEED),
)
# Use EdgePerformanceTier.CREATOR for mixed public catalog + private APIs,
# EdgePerformanceTier.LIVE for short-TTL / no-store live paths, or
# EdgePerformanceTier.VOD for Netflix-class catalogue + playback split (long
# edge SWR on metadata, private playback/license APIs, immutable posters).
```

Pair with **`CompressionPreset`**, **`ImmutableStaticCacheMiddleware`**, and **`ResponseCacheMiddleware`** for origin shielding.

### Factory helpers

```python
from fastmiddleware import create_middleware, middleware, MiddlewareBuilder, quick_middleware
```

Use these when you need a small custom middleware without a new module file.

## Related packages

- **`fastx_tenancy`** — `TenantMiddleware` and tenant context (different concern).
- **`fastx_platform`** — app config; not HTTP middleware.
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
