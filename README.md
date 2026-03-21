# fastmvc_middleware

**HTTP middleware for FastAPI / Starlette** — a large collection of production-oriented middlewares (security, CORS, rate limiting, auth, logging, tracing, caching, compression, health checks, graceful shutdown, and more) exposed from the **`fastmiddleware`** package, plus factories such as **`MiddlewareBuilder`** and **`create_middleware`**.

This package is **not** the same as **`fastmvc_tenancy`** (tenant resolution) or **`fastmvc_core`** (configuration DTOs); it focuses on **cross-cutting ASGI behavior** you mount on your FastAPI app.

## Layout

- `fastmiddleware/` — implementation modules (e.g. `cors`, `logging`, `rate_limit`, `security`, `authentication`, …).
- `tests/` — pytest suites per middleware area.

Install path depends on how your environment maps this repo (see `requirements.txt` or your app’s dependency list).

## Install

From the monorepo (if your project vendors this tree):

```bash
pip install -e ./fastmvc_middleware
```

## Related packages

- **`fastmvc_tenancy`** — `TenantMiddleware` and tenant context (different concern).
- **`fastmvc_core`** — app config; not HTTP middleware.
- Monorepo: [../README.md](../README.md).

## Tooling

If this folder includes [CONTRIBUTING.md](CONTRIBUTING.md), [Makefile](Makefile), and [PUBLISHING.md](PUBLISHING.md) (synced from tooling scripts), use them for tests and lint.
