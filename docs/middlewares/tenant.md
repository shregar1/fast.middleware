# TenantMiddleware

Multi-tenancy middleware for SaaS applications.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import TenantMiddleware, TenantConfig, get_tenant_id, get_tenant

app = FastAPI()

# Header-based tenant
app.add_middleware(
    TenantMiddleware,
    header_name="X-Tenant-ID",
)

# Subdomain-based tenant
app.add_middleware(
    TenantMiddleware,
    use_subdomain=True,
)

# Path-based tenant
app.add_middleware(
    TenantMiddleware,
    use_path=True,
    path_prefix="/tenant/",
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `header_name` | `str` | `"X-Tenant-ID"` | Header containing tenant ID |
| `use_subdomain` | `bool` | `False` | Extract from subdomain |
| `use_path` | `bool` | `False` | Extract from URL path |
| `path_prefix` | `str` | `"/tenant/"` | Path prefix to strip |
| `required` | `bool` | `True` | Require tenant ID |
| `exclude_paths` | `Set[str]` | `set()` | Paths without tenant |

## Tenant Extraction

### From Header

```bash
curl -H "X-Tenant-ID: acme-corp" https://api.example.com/data

```

### From Subdomain

```bash
curl https://acme-corp.api.example.com/data

# Tenant ID: "acme-corp"

```

### From Path

```bash
curl https://api.example.com/tenant/acme-corp/data

# Tenant ID: "acme-corp"

```

## Getting Tenant

```python
from fastmiddleware import get_tenant_id, get_tenant

@app.get("/data")
async def get_data():
    tenant_id = get_tenant_id()
    tenant = get_tenant()  # Full tenant object

    return await fetch_tenant_data(tenant_id)

# Or from request state
@app.get("/info")
async def get_info(request: Request):
    tenant_id = request.state.tenant_id
    return {"tenant": tenant_id}

```

## Custom Tenant Loading

```python
from fastmiddleware import TenantMiddleware

async def load_tenant(tenant_id: str):
    return await db.get_tenant(tenant_id)

app.add_middleware(
    TenantMiddleware,
    tenant_loader=load_tenant,
)

# Then access full tenant object
@app.get("/")
async def handler():
    tenant = get_tenant()  # Returns loaded tenant object
    return {"name": tenant.name}

```

## Response Codes

| Code | Description |
| ------ | ------------- |
| 400 | Missing tenant ID (if required) |
| 404 | Tenant not found (with loader) |

## Database Filtering

```python
@app.get("/items")
async def get_items():
    tenant_id = get_tenant_id()
    return await db.items.find({"tenant_id": tenant_id})

```

## Related Middlewares

- [SessionMiddleware](session.md)
- [ContextMiddleware](context.md)
