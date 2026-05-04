# HATEOASMiddleware

Hypermedia as the Engine of Application State middleware.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import HATEOASMiddleware, HATEOASConfig, Link

app = FastAPI()

# Basic usage
app.add_middleware(
    HATEOASMiddleware,
    link_generators={
        "/api/users": [
            Link(rel="self", href="/api/users", method="GET"),
            Link(rel="create", href="/api/users", method="POST", title="Create user"),
        ],
        "/api/products": [
            Link(rel="self", href="/api/products", method="GET"),
            Link(rel="search", href="/api/products/search", method="GET"),
        ],
    },
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `link_generators` | `Dict[str, List[Link]]` | `{}` | Path to links mapping |
| `link_key` | `str` | `"_links"` | Key for links in response |
| `self_link` | `bool` | `True` | Auto-add self link |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## Link Options

| Parameter | Type | Description |
| ----------- | ------ | ------------- |
| `rel` | `str` | Relationship type |
| `href` | `str` | Link URL |
| `method` | `str` | HTTP method |
| `title` | `str` | Human-readable title |

## Response Format

Original response:

```json
{"id": 1, "name": "John"}

```

With HATEOAS:

```json
{
  "id": 1,
  "name": "John",
  "_links": [
    {"rel": "self", "href": "https://api.example.com/api/users/1", "method": "GET"},
    {"rel": "update", "href": "https://api.example.com/api/users/1", "method": "PUT"},
    {"rel": "delete", "href": "https://api.example.com/api/users/1", "method": "DELETE"}
  ]
}

```

## Collection Response

Array responses are wrapped:

```json
{
  "items": [{"id": 1}, {"id": 2}],
  "_links": [
    {"rel": "self", "href": "https://api.example.com/api/users", "method": "GET"},
    {"rel": "create", "href": "https://api.example.com/api/users", "method": "POST"}
  ]
}

```

## Common Link Relations

| Relation | Description |
| ---------- | ------------- |
| `self` | Current resource |
| `create` | Create new resource |
| `update` | Update resource |
| `delete` | Delete resource |
| `collection` | Parent collection |
| `next` | Next page |
| `prev` | Previous page |
| `first` | First page |
| `last` | Last page |
| `search` | Search endpoint |

## Dynamic Links

For item-specific links, add them in your route handler:

```python
@app.get("/api/users/{user_id}")
async def get_user(user_id: int, request: Request):
    user = await get_user_by_id(user_id)

    return {
        **user,
        "_links": [
            {"rel": "self", "href": f"/api/users/{user_id}"},
            {"rel": "orders", "href": f"/api/users/{user_id}/orders"},
            {"rel": "update", "href": f"/api/users/{user_id}", "method": "PUT"},
        ],
    }

```

## Related Middlewares

- [VersioningMiddleware](versioning.md)
- [ContentNegotiationMiddleware](content-negotiation.md)
