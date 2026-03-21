"""Security headers middleware."""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fastmvc_middleware import SecurityHeadersConfig, SecurityHeadersMiddleware


async def ok(_request: Request):
    return PlainTextResponse("ok")


def test_security_headers_defaults():
    app = Starlette(routes=[Route("/", ok)])
    app.add_middleware(SecurityHeadersMiddleware)
    client = TestClient(app)
    r = client.get("/")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
    assert "frame-ancestors" in r.headers.get("Content-Security-Policy", "")
    assert "Strict-Transport-Security" not in r.headers


def test_security_headers_hsts_and_no_csp():
    app = Starlette(routes=[Route("/", ok)])
    app.add_middleware(
        SecurityHeadersMiddleware,
        config=SecurityHeadersConfig(
            hsts_max_age=31536000,
            hsts_include_subdomains=True,
            csp_frame_ancestors=None,
            x_frame_options="SAMEORIGIN",
        ),
    )
    client = TestClient(app)
    r = client.get("/")
    assert r.headers["Strict-Transport-Security"].startswith("max-age=31536000")
    assert "includeSubDomains" in r.headers["Strict-Transport-Security"]
    assert "Content-Security-Policy" not in r.headers
    assert r.headers.get("X-Frame-Options") == "SAMEORIGIN"
