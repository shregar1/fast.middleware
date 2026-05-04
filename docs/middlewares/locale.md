# LocaleMiddleware

Detect and manage user locale for internationalization.

## Installation

```bash
pip install fastx-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import LocaleMiddleware, get_locale

app = FastAPI()

app.add_middleware(
    LocaleMiddleware,
    supported_locales=["en-US", "es-ES", "fr-FR", "de-DE"],
    default_locale="en-US",
)

@app.get("/")
async def handler():
    locale = get_locale()
    return {"locale": locale}

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `supported_locales` | `list[str]` | `["en"]` | Supported locale codes |
| `default_locale` | `str` | `"en"` | Default when no match |
| `cookie_name` | `str` | `"locale"` | Cookie name for persistence |
| `query_param` | `str` | `"lang"` | Query parameter name |

## Locale Detection Priority

1. Query parameter (`?lang=es`)
2. Cookie (`locale=es-ES`)
3. Accept-Language header
4. Default locale

## Helper Functions

### `get_locale() -> str`

Returns the detected locale for the current request.

```python
from fastmiddleware import get_locale

@app.get("/content")
async def content():
    locale = get_locale()
    return load_content(locale)

```

## Examples

### Basic Locale Detection

```python
app.add_middleware(
    LocaleMiddleware,
    supported_locales=["en", "es", "fr"],
    default_locale="en",
)

# Accept-Language: es,en;q=0.9

# get_locale() returns: "es"

```

### With Region Codes

```python
app.add_middleware(
    LocaleMiddleware,
    supported_locales=["en-US", "en-GB", "es-ES", "es-MX", "fr-FR", "fr-CA"],
    default_locale="en-US",
)

```

### Persistent Locale (Cookie)

```python
@app.post("/set-locale")
async def set_locale(locale: str, response: Response):
    if locale in ["en", "es", "fr"]:
        response.set_cookie("locale", locale, max_age=31536000)
        return {"locale": locale}
    raise HTTPException(400, "Invalid locale")

```

### Translation Integration

```python
from fastmiddleware import LocaleMiddleware, get_locale
import gettext

app.add_middleware(
    LocaleMiddleware,
    supported_locales=["en", "es", "fr"],
)

def get_translator():
    locale = get_locale()
    return gettext.translation('messages', 'locales', [locale], fallback=True)

@app.get("/messages")
async def messages():
    _ = get_translator().gettext
    return {
        "welcome": _("Welcome"),
        "goodbye": _("Goodbye"),
    }

```

### Currency and Date Formatting

```python
from babel import numbers, dates
from fastmiddleware import get_locale

@app.get("/product/{id}")
async def product(id: str):
    locale = get_locale()
    product = await get_product(id)

    return {
        "name": product.name,
        "price": numbers.format_currency(product.price, "USD", locale=locale),
        "created": dates.format_date(product.created, locale=locale),
    }

```

### Override via Query Parameter

```python

# GET /page?lang=es

# get_locale() returns: "es"

# (even if Accept-Language is "en")

```

## Request State

```python
request.state.locale      # The detected locale
request.state.locale_source  # "query", "cookie", "header", or "default"

```

## Related Middlewares

- [AcceptLanguageMiddleware](accept-language.md) - Language-only negotiation
- [GeoIPMiddleware](geoip.md) - GeoIP detection
