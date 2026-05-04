# SessionMiddleware

Server-side session management middleware.

## Prerequisites

✅ No additional dependencies required.

## Installation

```bash
pip install fastx-middleware

```

## Usage

```python
from fastapi import FastAPI
from fastmiddleware import SessionMiddleware, SessionConfig

app = FastAPI()

# Basic usage
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key-min-32-chars-long",
)

# With config
config = SessionConfig(
    secret_key="your-secret-key",
    cookie_name="session_id",
    max_age=3600,  # 1 hour
    cookie_secure=True,
    cookie_httponly=True,
    cookie_samesite="lax",
)
app.add_middleware(SessionMiddleware, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `secret_key` | `str` | Required | Secret for session signing |
| `cookie_name` | `str` | `"session_id"` | Session cookie name |
| `max_age` | `int` | `3600` | Session lifetime in seconds |
| `cookie_secure` | `bool` | `True` | Secure flag |
| `cookie_httponly` | `bool` | `True` | HTTPOnly flag |
| `cookie_samesite` | `str` | `"lax"` | SameSite attribute |
| `exclude_paths` | `Set[str]` | `set()` | Paths without session |

## Using Sessions

```python
from fastapi import Request

@app.get("/")
async def handler(request: Request):
    session = request.state.session

    # Get value
    user_id = session.get("user_id")

    # Set value
    session.set("user_id", 123)
    session["visits"] = session.get("visits", 0) + 1

    # Delete value
    session.delete("temp_data")

    # Clear all
    session.clear()

    return {"user_id": user_id}

```

## Session API

| Method | Description |
| -------- | ------------- |
| `session.get(key, default=None)` | Get value |
| `session.set(key, value)` | Set value |
| `session[key] = value` | Set value (dict-style) |
| `session.delete(key)` | Delete key |
| `session.clear()` | Clear all data |
| `session.regenerate()` | New session ID |

## Custom Session Store

```python
from fastmiddleware import SessionStore, Session

class RedisSessionStore(SessionStore):
    async def load(self, session_id: str) -> Session:
        data = await redis.get(f"session:{session_id}")
        return Session(session_id, json.loads(data) if data else {})

    async def save(self, session: Session) -> None:
        await redis.set(
            f"session:{session.id}",
            json.dumps(session.data),
            ex=3600,
        )

    async def delete(self, session_id: str) -> None:
        await redis.delete(f"session:{session_id}")

app.add_middleware(
    SessionMiddleware,
    secret_key="secret",
    store=RedisSessionStore(),
)

```

## Related Middlewares

- [CSRFMiddleware](csrf.md) - Uses session for tokens
- [AuthenticationMiddleware](authentication.md)
