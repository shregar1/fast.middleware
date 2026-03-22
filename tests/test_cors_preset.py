"""CORSPreset DTO."""

from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

from fastmiddleware import CORSPreset


def test_cors_preset_starlette_kwargs():
    p = CORSPreset()
    kw = p.starlette_kwargs()
    assert "http://localhost:3000" in kw["allow_origins"]
    assert kw["allow_credentials"] is True
    assert "GET" in kw["allow_methods"]


def test_cors_middleware_with_preset():
    from starlette.applications import Starlette
    from starlette.responses import PlainTextResponse
    from starlette.routing import Route

    async def home(_):
        return PlainTextResponse("ok")

    app = Starlette(routes=[Route("/", home)])
    preset = CORSPreset(allow_origins=["https://app.example.com"], allow_credentials=True)
    app.add_middleware(CORSMiddleware, **preset.starlette_kwargs())
    client = TestClient(app)
    r = client.get("/", headers={"Origin": "https://app.example.com"})
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-origin") == "https://app.example.com"
