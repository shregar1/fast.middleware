# FeatureFlagMiddleware

Feature flag management middleware.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fast-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import FeatureFlagMiddleware, FeatureFlagConfig, is_feature_enabled, get_feature_flags

app = FastAPI()

# Basic usage with static flags
app.add_middleware(
    FeatureFlagMiddleware,
    flags={
        "new_dashboard": True,
        "dark_mode": False,
        "beta_features": True,
    },
)

# With config
config = FeatureFlagConfig(
    flags={
        "new_dashboard": True,
        "dark_mode": False,
    },
    header_overrides=True,  # Allow X-Feature-Flags header
)
app.add_middleware(FeatureFlagMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `flags` | `Dict[str, bool]` | `{}` | Feature flag values |
| `header_overrides` | `bool` | `False` | Allow header overrides |
| `override_header` | `str` | `"X-Feature-Flags"` | Override header name |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## Checking Flags

```python
from fastmiddleware import is_feature_enabled, get_feature_flags

@app.get("/dashboard")
async def dashboard():
    if is_feature_enabled("new_dashboard"):
        return new_dashboard_response()
    return old_dashboard_response()

@app.get("/features")
async def features():
    flags = get_feature_flags()
    return {"features": flags}

```

## Header Overrides

For testing, clients can override flags:

```bash
curl -H "X-Feature-Flags: new_dashboard=true,dark_mode=true" https://api.example.com/

```

## Dynamic Flags

```python
middleware = FeatureFlagMiddleware(app, flags={})

# Update flags at runtime
middleware.set_flag("new_feature", True)
middleware.set_flag("old_feature", False)

# Get current flags
current = middleware.get_flags()

```

## Accessing in Request

```python
@app.get("/")
async def handler(request: Request):
    flags = request.state.feature_flags
    return {"dark_mode": flags.get("dark_mode", False)}

```

## Related Middlewares

- [ABTestMiddleware](ab-testing.md) - A/B testing
