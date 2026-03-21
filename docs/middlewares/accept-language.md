# AcceptLanguageMiddleware

Parse and negotiate Accept-Language headers for internationalization.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import AcceptLanguageMiddleware, get_language

app = FastAPI()

app.add_middleware(
    AcceptLanguageMiddleware,
    supported_languages=["en", "es", "fr", "de"],
    default_language="en",
)

@app.get("/")
async def handler():
    lang = get_language()
    return {"language": lang}

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `supported_languages` | `list[str]` | `["en"]` | Languages your app supports |
| `default_language` | `str` | `"en"` | Fallback when no match found |

## How It Works

1. Parses the `Accept-Language` header from the request
2. Matches against your supported languages (with quality weights)
3. Falls back to default if no match
4. Makes language available via `get_language()`

## Helper Functions

### `get_language() -> str`

Returns the negotiated language code for the current request.

```python
from fastmiddleware import get_language

@app.get("/greeting")
async def greeting():
    lang = get_language()

    greetings = {
        "en": "Hello!",
        "es": "¡Hola!",
        "fr": "Bonjour!",
        "de": "Hallo!",
    }

    return {"message": greetings.get(lang, greetings["en"])}

```

## Examples

### Basic Language Detection

```python
app.add_middleware(
    AcceptLanguageMiddleware,
    supported_languages=["en", "es", "fr"],
    default_language="en",
)

# Request with: Accept-Language: es,en;q=0.9

# get_language() returns: "es"

```

### With Locale Variants

```python
app.add_middleware(
    AcceptLanguageMiddleware,
    supported_languages=["en-US", "en-GB", "es-ES", "es-MX"],
    default_language="en-US",
)

```

### Integration with Translation System

```python
from fastmiddleware import AcceptLanguageMiddleware, get_language
import gettext

app.add_middleware(
    AcceptLanguageMiddleware,
    supported_languages=["en", "es", "fr"],
)

@app.get("/translate")
async def translate():
    lang = get_language()
    translator = gettext.translation('messages', localedir='locales', languages=[lang])
    _ = translator.gettext

    return {"message": _("Welcome to our API")}

```

## Related Middlewares

- [LocaleMiddleware](locale.md) - Full locale detection with region
- [ContentNegotiationMiddleware](content-negotiation.md) - Content type negotiation
