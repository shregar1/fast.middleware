"""Tests for CDN edge performance tier presets and middleware."""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fastmiddleware import (
    EdgePerformanceTier,
    EdgeTierCacheHeadersConfig,
    EdgeTierCacheHeadersMiddleware,
    tier_definition,
)


async def _hello(_: Request):
    """Execute _hello operation.

    Args:
        _: The _ parameter.

    Returns:
        The result of the operation.
    """
    return PlainTextResponse("ok")


def test_tier_definition_feed_has_swr():
    """Execute test_tier_definition_feed_has_swr operation.

    Returns:
        The result of the operation.
    """
    d = tier_definition(EdgePerformanceTier.FEED)
    assert "stale-while-revalidate" in d.default_cache_control
    assert d.cdn_cache_control
    assert "/static/" in [p for p, _ in d.path_overrides]


def test_tier_definition_creator_private_default():
    """Execute test_tier_definition_creator_private_default operation.

    Returns:
        The result of the operation.
    """
    d = tier_definition(EdgePerformanceTier.CREATOR)
    assert "private" in d.default_cache_control
    assert any("/api/public/" in p for p, _ in d.path_overrides)


def test_tier_definition_live_short_ttl():
    """Execute test_tier_definition_live_short_ttl operation.

    Returns:
        The result of the operation.
    """
    d = tier_definition(EdgePerformanceTier.LIVE)
    assert "no-store" in next(v for p, v in d.path_overrides if "live" in p)


def test_tier_definition_vod_netflix_class():
    """Execute test_tier_definition_vod_netflix_class operation.

    Returns:
        The result of the operation.
    """
    d = tier_definition(EdgePerformanceTier.VOD)
    assert "604800" in d.default_cache_control
    assert "Accept-Language" in d.vary
    assert any("playback" in p for p, _ in d.path_overrides)
    pb = next(v for p, v in d.path_overrides if "playback" in p)
    assert "no-store" in pb
    cat = next(v for p, v in d.path_overrides if "catalog" in p)
    assert "stale-while-revalidate" in cat


def test_middleware_sets_cache_control_feed():
    """Execute test_middleware_sets_cache_control_feed operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/feed", _hello)])
    app.add_middleware(
        EdgeTierCacheHeadersMiddleware,
        config=EdgeTierCacheHeadersConfig(tier=EdgePerformanceTier.FEED),
    )
    client = TestClient(app)
    r = client.get("/feed")
    assert r.status_code == 200
    assert "stale-while-revalidate" in r.headers["cache-control"]
    assert "CDN-Cache-Control" in r.headers or "cache-control" in r.headers


def test_middleware_respects_static_override():
    """Execute test_middleware_respects_static_override operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/static/app.js", _hello)])
    app.add_middleware(
        EdgeTierCacheHeadersMiddleware,
        config=EdgeTierCacheHeadersConfig(tier=EdgePerformanceTier.FEED),
    )
    client = TestClient(app)
    r = client.get("/static/app.js")
    assert "immutable" in r.headers["cache-control"]


def test_middleware_skips_docs_prefix():
    """Execute test_middleware_skips_docs_prefix operation.

    Returns:
        The result of the operation.
    """
    app = Starlette(routes=[Route("/docs", _hello)])
    app.add_middleware(
        EdgeTierCacheHeadersMiddleware,
        config=EdgeTierCacheHeadersConfig(tier=EdgePerformanceTier.FEED),
    )
    client = TestClient(app)
    r = client.get("/docs")
    assert not r.headers.get("cache-control")
