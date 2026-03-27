"""Body size limit middleware."""

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fastmiddleware import BodySizeLimitMiddleware


async def echo(_):
    """Execute echo operation.

    Args:
        _: The _ parameter.

    Returns:
        The result of the operation.
    """
    return PlainTextResponse("ok")


def test_rejects_large_content_length():
    """Execute test_rejects_large_content_length operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/", echo, methods=["POST", "GET"])])
    app.add_middleware(BodySizeLimitMiddleware, max_bytes=100)
    client = TestClient(app)
    r = client.post("/", headers={"Content-Length": "500"}, content=b"")
    assert r.status_code == 413


def test_allows_small_body():
    """Execute test_allows_small_body operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/", echo, methods=["POST", "GET"])])
    app.add_middleware(BodySizeLimitMiddleware, max_bytes=10_000)
    client = TestClient(app)
    r = client.post("/", content=b"small")
    assert r.status_code == 200


def test_invalid_content_length_400():
    """Execute test_invalid_content_length_400 operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/", echo, methods=["POST", "GET"])])
    app.add_middleware(BodySizeLimitMiddleware, max_bytes=1000)
    client = TestClient(app)
    r = client.post("/", headers={"Content-Length": "not-a-number"}, content=b"x")
    assert r.status_code == 400
