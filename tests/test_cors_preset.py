"""CORSPreset DTO."""

from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

from fastmiddleware import CORSPreset


def test_cors_preset_starlette_kwargs():
    """Execute test_cors_preset_starlette_kwargs operation.

    Returns:
        The result of the operation.
    """
    p = CORSPreset()
    kw = p.starlette_kwargs()
    assert "http://localhost:3000" in kw["allow_origins"]
    assert kw["allow_credentials"] is True
    assert "GET" in kw["allow_methods"]


def test_cors_middleware_with_preset():
    """Execute test_cors_middleware_with_preset operation.

    Returns:
        The result of the operation.
    """
    from starlette.applications import Starlette
    from starlette.responses import PlainTextResponse
    from starlette.routing import Route

    async def home(_):
        """Execute home operation.

        Args:
            _: The _ parameter.

        Returns:
            The result of the operation.
        """
        return PlainTextResponse("ok")

    app = Starlette(routes=[Route("/", home)])
    preset = CORSPreset(
        allow_origins=["https://app.example.com"], allow_credentials=True
    )
    app.add_middleware(CORSMiddleware, **preset.starlette_kwargs())
    client = TestClient(app)
    r = client.get("/", headers={"Origin": "https://app.example.com"})
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-origin") == "https://app.example.com"
