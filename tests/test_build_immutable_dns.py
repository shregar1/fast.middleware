"""Tests for BuildVersion, ImmutableStaticCache, and DNSPrefetchControl middleware."""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fastmiddleware import (
    BuildVersionConfig,
    BuildVersionMiddleware,
    DNSPrefetchControlConfig,
    DNSPrefetchControlMiddleware,
    ImmutableStaticCacheConfig,
    ImmutableStaticCacheMiddleware,
)


async def _hello(_: Request) -> PlainTextResponse:
    """Execute _hello operation.

    Args:
        _: The _ parameter.

    Returns:
        The result of the operation.
    """
    return PlainTextResponse("ok")


def test_build_version_from_explicit_config():
    """Execute test_build_version_from_explicit_config operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/", _hello)])
    app.add_middleware(
        BuildVersionMiddleware,
        config=BuildVersionConfig(version="9.9.9", git_sha="abc1234"),
    )
    client = TestClient(app)
    r = client.get("/")
    assert r.headers["X-App-Version"] == "9.9.9"
    assert r.headers["X-Git-SHA"] == "abc1234"


def test_build_version_from_env(monkeypatch):
    """Execute test_build_version_from_env operation.

    Args:
        monkeypatch: The monkeypatch parameter.

    Returns:
        The result of the operation.
    """
    monkeypatch.setenv("APP_VERSION", " 1.2.3 ")
    monkeypatch.setenv("GIT_SHA", "deadbeef")
    app = Starlette(routes=[Route("/", _hello)])
    app.add_middleware(BuildVersionMiddleware)
    client = TestClient(app)
    r = client.get("/")
    assert r.headers["X-App-Version"] == "1.2.3"
    assert r.headers["X-Git-SHA"] == "deadbeef"


def test_build_version_skips_empty_without_include_empty(monkeypatch):
    """Execute test_build_version_skips_empty_without_include_empty operation.

    Args:
        monkeypatch: The monkeypatch parameter.

    Returns:
        The result of the operation.
    """
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("GIT_SHA", raising=False)
    app = Starlette(routes=[Route("/", _hello)])
    app.add_middleware(BuildVersionMiddleware)
    client = TestClient(app)
    r = client.get("/")
    assert "X-App-Version" not in r.headers
    assert "X-Git-SHA" not in r.headers


def test_immutable_static_cache_on_prefix():
    """Execute test_immutable_static_cache_on_prefix operation.

    Returns:
        The result of the operation.
    """

    async def asset(_: Request) -> PlainTextResponse:
        """Execute asset operation.

        Args:
            _: The _ parameter.

        Returns:
            The result of the operation.
        """
        return PlainTextResponse("x")

    app = Starlette(routes=[Route("/static/app.hash.js", asset)])
    app.add_middleware(ImmutableStaticCacheMiddleware)
    client = TestClient(app)
    r = client.get("/static/app.hash.js")
    assert "immutable" in r.headers["Cache-Control"]
    assert "public" in r.headers["Cache-Control"]
    assert "max-age=" in r.headers["Cache-Control"]


def test_immutable_static_skips_api():
    """Execute test_immutable_static_skips_api operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/api/x", _hello)])
    app.add_middleware(ImmutableStaticCacheMiddleware)
    client = TestClient(app)
    r = client.get("/api/x")
    assert "Cache-Control" not in r.headers


def test_dns_prefetch_off_by_default():
    """Execute test_dns_prefetch_off_by_default operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/", _hello)])
    app.add_middleware(DNSPrefetchControlMiddleware)
    client = TestClient(app)
    r = client.get("/")
    assert r.headers["X-DNS-Prefetch-Control"] == "off"


def test_dns_prefetch_custom():
    """Execute test_dns_prefetch_custom operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/", _hello)])
    app.add_middleware(
        DNSPrefetchControlMiddleware,
        config=DNSPrefetchControlConfig(value="on", header_name="X-DNS"),
    )
    client = TestClient(app)
    r = client.get("/")
    assert r.headers["X-DNS"] == "on"
