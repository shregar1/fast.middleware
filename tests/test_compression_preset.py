"""Compression preset (gzip)."""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fast_middleware import CompressionPreset


async def large(_):
    return JSONResponse({"data": "x" * 2000})


def test_compression_preset_adds_vary_or_encoding():
    app = Starlette(routes=[Route("/large", large)])
    CompressionPreset(enabled=True, minimum_size=100).add_to_app(app)
    client = TestClient(app)
    r = client.get("/large", headers={"Accept-Encoding": "gzip"})
    assert r.status_code == 200
    assert r.headers.get("Content-Encoding") == "gzip" or r.headers.get("Vary") == "Accept-Encoding"


def test_compression_disabled():
    app = Starlette(routes=[Route("/large", large)])
    CompressionPreset(enabled=False).add_to_app(app)
    client = TestClient(app)
    r = client.get("/large", headers={"Accept-Encoding": "gzip"})
    assert r.status_code == 200
    assert r.headers.get("Content-Encoding") != "gzip"
