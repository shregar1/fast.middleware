"""Tests for RequestIDMiddleware."""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from core.utils.request_id_context import RequestIdContext
from fastmiddleware import RequestIDMiddleware


async def homepage(_request: Request):
    """Execute homepage operation.

    Args:
        _request: The _request parameter.

    Returns:
        The result of the operation.
    """
    return PlainTextResponse(RequestIdContext.get() or "")


def _app():
    """Execute _app operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/", homepage)])
    app.add_middleware(RequestIDMiddleware)
    return app


def test_request_id_header_and_context_match():
    """Execute test_request_id_header_and_context_match operation.

    Returns:
        The result of the operation.
    """
    client = TestClient(_app())
    r = client.get("/")
    assert r.status_code == 200
    rid = r.headers["X-Request-ID"]
    assert rid
    assert r.text == rid


def test_accepts_incoming_request_id():
    """Execute test_accepts_incoming_request_id operation.

    Returns:
        The result of the operation.
    """
    client = TestClient(_app())
    r = client.get("/", headers={"X-Request-ID": "  from-client  "})
    assert r.headers["X-Request-ID"] == "from-client"
    assert r.text == "from-client"


def test_custom_id_factory():
    """Execute test_custom_id_factory operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/", homepage)])
    app.add_middleware(RequestIDMiddleware, id_factory=lambda: "fixed-id")
    client = TestClient(app)
    r = client.get("/")
    assert r.headers["X-Request-ID"] == "fixed-id"
    assert r.text == "fixed-id"
