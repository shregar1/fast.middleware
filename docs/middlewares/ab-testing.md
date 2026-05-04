# ABTestMiddleware

A/B testing middleware for experiments.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import ABTestMiddleware, ABTestConfig, Experiment, get_variant

app = FastAPI()

# Basic usage
app.add_middleware(
    ABTestMiddleware,
    experiments=[
        Experiment(
            name="checkout_flow",
            variants=["control", "variant_a", "variant_b"],
            weights=[0.5, 0.25, 0.25],  # 50%, 25%, 25%
        ),
        Experiment(
            name="pricing_page",
            variants=["original", "new_design"],
            weights=[0.5, 0.5],  # 50/50 split
        ),
    ],
)

```

## Configuration

### Experiment Options

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `name` | `str` | Required | Experiment identifier |
| `variants` | `List[str]` | Required | Variant names |
| `weights` | `List[float]` | Equal | Distribution weights |
| `enabled` | `bool` | `True` | Is experiment active |

### Middleware Options

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `experiments` | `List[Experiment]` | `[]` | Active experiments |
| `cookie_name` | `str` | `"ab_variants"` | Cookie for persistence |
| `cookie_max_age` | `int` | `2592000` | 30 days |
| `exclude_paths` | `Set[str]` | `set()` | Paths to exclude |

## Getting Variants

```python
from fastmiddleware import get_variant

@app.get("/checkout")
async def checkout():
    variant = get_variant("checkout_flow")

    if variant == "control":
        return control_checkout()
    elif variant == "variant_a":
        return variant_a_checkout()
    else:
        return variant_b_checkout()

```

## Variant Persistence

Variants are stored in cookies to ensure users see consistent experiences:

```python
@app.get("/")
async def handler(request: Request):
    variants = request.state.variants
    return {
        "checkout_flow": variants.get("checkout_flow"),
        "pricing_page": variants.get("pricing_page"),
    }

```

## Force Variant (Testing)

```bash

# Force specific variant via query param
curl "https://api.example.com/?ab_checkout_flow=variant_a"

```

## Analytics Integration

```python
@app.get("/purchase")
async def purchase(request: Request):
    variant = get_variant("checkout_flow")

    # Track conversion with variant
    analytics.track("purchase", {
        "variant": variant,
        "experiment": "checkout_flow",
    })

    return {"success": True}

```

## Related Middlewares

- [FeatureFlagMiddleware](feature-flag.md)
- [RequestSamplerMiddleware](request-sampler.md)
