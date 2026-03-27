"""Compression preset (gzip)."""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fastmiddleware import CompressionPreset


async def large(_):
    """Execute large operation.

    Args:
        _: The _ parameter.

    Returns:
        The result of the operation.
    """
    return JSONResponse({"data": "x" * 2000})


def test_compression_preset_adds_vary_or_encoding():
    """Execute test_compression_preset_adds_vary_or_encoding operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/large", large)])
    CompressionPreset(enabled=True, minimum_size=100).add_to_app(app)
    client = TestClient(app)
    r = client.get("/large", headers={"Accept-Encoding": "gzip"})
    assert r.status_code == 200
    assert (
        r.headers.get("Content-Encoding") == "gzip"
        or r.headers.get("Vary") == "Accept-Encoding"
    )


def test_compression_disabled():
    """Execute test_compression_disabled operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/large", large)])
    CompressionPreset(enabled=False).add_to_app(app)
    client = TestClient(app)
    r = client.get("/large", headers={"Accept-Encoding": "gzip"})
    assert r.status_code == 200
    assert r.headers.get("Content-Encoding") != "gzip"
