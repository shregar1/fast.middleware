"""Edge performance tiers inspired by large-scale consumer platforms.

These are **HTTP cache semantics** for FastAPI/Starlette behind a CDN or reverse
proxy—not full platform replication. Use with:

- **CDN** (Cloudflare, Fastly, Akamai, CloudFront) honoring ``s-maxage``,
  ``stale-while-revalidate``, ``CDN-Cache-Control``, ``Surrogate-Control``.
- **Compression** (:class:`~fastmiddleware.mw_core.compression.CompressionPreset`).
- **Immutable static** (:class:`~fastmiddleware.operations.immutable_static_cache.ImmutableStaticCacheMiddleware`).
- **Response cache** (:class:`~fastmiddleware.operations.response_cache.ResponseCacheMiddleware`) for origin shielding.

Tiers (names are analogies; tune paths/TTLs for your product):

- **FEED** — Timeline / UGC read paths: long **stale-while-revalidate** at the edge
  (Instagram-class feed behavior: serve stale while revalidating).
- **CREATOR** — Mixed public catalog + private account APIs (creator economy platforms:
  default **private, no-store**; opt-in **public** prefixes for marketing/thumbnails).
- **LIVE** — Presence, live status, WebSocket-adjacent HTTP polls: **short TTL** or
  **no-store** (Twitch-class: minimize stale live state).
- **VOD** — Catalogue + on-demand streaming HTTP: **long edge SWR** for metadata rows,
  **private / no-store** for playback & rights, **immutable** posters, **short TTL**
  for segment-like paths (Netflix-class Open Connect style **cache semantics**).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from enum import Enum

from starlette.requests import Request
from starlette.responses import Response

from fastmiddleware.mw_core.base import FastMVCMiddleware


class EdgePerformanceTier(str, Enum):
    """Named edge caching strategies (analogies to well-known product classes)."""

    FEED = "feed"
    """Instagram-class: feed & read-heavy graphs; aggressive SWR at CDN."""

    CREATOR = "creator"
    """OnlyFans-class: monetized creator surfaces; split public vs authenticated cache."""

    VOD = "vod"
    """Netflix-class: catalogue + binge; long edge SWR on metadata, private playback/DRM APIs."""

    LIVE = "live"
    """Twitch-class: live status, presence, low-latency reads; minimal caching."""


@dataclass(frozen=True)
class EdgeTierDefinition:
    """Header bundle for one tier.

    * ``default_cache_control`` — applied when no path override matches and the
      response has no ``Cache-Control`` yet.
    * ``cdn_cache_control`` — optional ``CDN-Cache-Control`` (Cloudflare, some stacks).
    * ``surrogate_control`` — optional ``Surrogate-Control`` (Fastly/Akamai style).
    * ``vary`` — ``Vary`` header when absent (helps caches key correctly).
    * ``path_overrides`` — longest-prefix wins: ``(prefix, cache-control value)``.
    """

    title: str
    default_cache_control: str
    cdn_cache_control: str | None = None
    surrogate_control: str | None = None
    vary: str = "Accept-Encoding"
    path_overrides: tuple[tuple[str, str], ...] = ()


def tier_definition(tier: EdgePerformanceTier) -> EdgeTierDefinition:
    """Return the built-in preset for *tier* (override by building your own middleware config)."""
    if tier is EdgePerformanceTier.FEED:
        return EdgeTierDefinition(
            title="Feed / social timeline (Instagram-class)",
            default_cache_control=(
                "public, max-age=0, s-maxage=120, "
                "stale-while-revalidate=86400, stale-if-error=604800"
            ),
            cdn_cache_control=(
                "public, max-age=0, s-maxage=120, stale-while-revalidate=86400"
            ),
            surrogate_control="max-age=0, stale-while-revalidate=86400",
            vary="Accept-Encoding, Accept",
            path_overrides=(
                ("/static/", "public, max-age=31536000, immutable"),
                ("/assets/", "public, max-age=31536000, immutable"),
            ),
        )

    if tier is EdgePerformanceTier.CREATOR:
        return EdgeTierDefinition(
            title="Creator / subscription mix (creator-platform-class)",
            default_cache_control="private, no-store",
            cdn_cache_control="private, no-store",
            vary="Accept-Encoding, Authorization",
            path_overrides=(
                ("/api/public/", "public, s-maxage=300, stale-while-revalidate=3600"),
                (
                    "/public/",
                    "public, max-age=60, s-maxage=600, stale-while-revalidate=86400",
                ),
                ("/static/", "public, max-age=31536000, immutable"),
            ),
        )

    if tier is EdgePerformanceTier.VOD:
        return EdgeTierDefinition(
            title="VOD / binge catalogue (Netflix-class)",
            default_cache_control=(
                "public, max-age=0, s-maxage=600, "
                "stale-while-revalidate=604800, stale-if-error=2592000"
            ),
            cdn_cache_control=(
                "public, max-age=0, s-maxage=600, stale-while-revalidate=604800"
            ),
            surrogate_control="max-age=0, stale-while-revalidate=604800",
            vary="Accept-Encoding, Accept-Language",
            path_overrides=(
                ("/api/playback/", "private, no-store"),
                ("/api/license/", "private, no-store"),
                ("/api/drm/", "private, no-store"),
                ("/api/session/", "private, no-store"),
                ("/api/entitlement/", "private, no-store"),
                (
                    "/api/catalog/",
                    "public, s-maxage=1800, stale-while-revalidate=604800",
                ),
                (
                    "/api/metadata/",
                    "public, s-maxage=3600, stale-while-revalidate=604800",
                ),
                (
                    "/api/recommendations/",
                    "public, max-age=0, s-maxage=120, stale-while-revalidate=3600",
                ),
                ("/images/", "public, max-age=31536000, immutable"),
                ("/img/", "public, max-age=31536000, immutable"),
                ("/static/", "public, max-age=31536000, immutable"),
                ("/assets/", "public, max-age=31536000, immutable"),
                (
                    "/media/",
                    "public, max-age=8, s-maxage=86400, stale-while-revalidate=3600",
                ),
            ),
        )

    if tier is EdgePerformanceTier.LIVE:
        return EdgeTierDefinition(
            title="Live / realtime HTTP (Twitch-class)",
            default_cache_control="public, max-age=0, s-maxage=5, must-revalidate",
            cdn_cache_control="public, max-age=0, s-maxage=5, must-revalidate",
            surrogate_control="max-age=5",
            vary="Accept-Encoding",
            path_overrides=(
                ("/api/live/", "no-store"),
                ("/api/presence/", "private, max-age=0, s-maxage=2, must-revalidate"),
                ("/static/", "public, max-age=31536000, immutable"),
            ),
        )

    raise ValueError(f"unknown tier: {tier!r}")


@dataclass
class EdgeTierCacheHeadersConfig:
    """Apply tier-based cache headers to GET/HEAD responses when not already set.

    Attributes:
        tier: Built-in preset (see :class:`EdgePerformanceTier`).
        definition: Optional full override of headers/path rules.
        only_if_missing: If True (default), do not overwrite existing ``Cache-Control``.
        set_cdn_headers: Emit ``CDN-Cache-Control`` / ``Surrogate-Control`` when defined.

    """

    tier: EdgePerformanceTier = EdgePerformanceTier.FEED
    definition: EdgeTierDefinition | None = None
    only_if_missing: bool = True
    set_cdn_headers: bool = True
    exclude_paths: set[str] = field(default_factory=set)
    exclude_prefixes: tuple[str, ...] = (
        "/docs",
        "/openapi",
        "/redoc",
        "/health",
        "/metrics",
    )


def _path_under_prefix(path: str, prefix: str) -> bool:
    """True if *path* equals *prefix* or is a deeper path under it."""
    base = prefix.rstrip("/")
    if not base:
        return False
    if path == base:
        return True
    return path.startswith(base + "/")


def _longest_prefix_match(path: str, rules: tuple[tuple[str, str], ...]) -> str | None:
    """Execute _longest_prefix_match operation.

    Args:
        path: The path parameter.
        rules: The rules parameter.

    Returns:
        The result of the operation.
    """
    best: tuple[int, str] | None = None
    for prefix, value in rules:
        if _path_under_prefix(path, prefix):
            plen = len(prefix.rstrip("/"))
            if best is None or plen > best[0]:
                best = (plen, value)
    return best[1] if best else None


class EdgeTierCacheHeadersMiddleware(FastMVCMiddleware):
    """Apply **CDN-oriented** cache headers from a tier preset.

    Safe defaults: does not replace ``Cache-Control`` already set by handlers when
    ``only_if_missing`` is True.

    Example::

        from fastmiddleware import EdgePerformanceTier, EdgeTierCacheHeadersMiddleware

        app.add_middleware(
            EdgeTierCacheHeadersMiddleware,
            config=EdgeTierCacheHeadersConfig(tier=EdgePerformanceTier.VOD),
        )
    """

    def __init__(
        self,
        app,
        config: EdgeTierCacheHeadersConfig | None = None,
        *,
        tier: EdgePerformanceTier | None = None,
        exclude_paths: set[str] | None = None,
        exclude_prefixes: tuple[str, ...] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            tier: The tier parameter.
            exclude_paths: The exclude_paths parameter.
            exclude_prefixes: The exclude_prefixes parameter.
        """
        super().__init__(app)
        self.config = config or EdgeTierCacheHeadersConfig()
        if tier is not None:
            self.config.tier = tier
        if exclude_paths is not None:
            self.config.exclude_paths = exclude_paths
        if exclude_prefixes is not None:
            self.config.exclude_prefixes = exclude_prefixes
        self._def = self.config.definition or tier_definition(self.config.tier)

    def _skip_path(self, path: str) -> bool:
        """Execute _skip_path operation.

        Args:
            path: The path parameter.

        Returns:
            The result of the operation.
        """
        if path in self.config.exclude_paths:
            return True
        return any(path.startswith(p) for p in self.config.exclude_prefixes)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Execute dispatch operation.

        Args:
            request: The request parameter.
            call_next: The call_next parameter.

        Returns:
            The result of the operation.
        """
        if self.should_skip(request):
            return await call_next(request)

        response = await call_next(request)

        if request.method not in ("GET", "HEAD"):
            return response
        if self._skip_path(request.url.path):
            return response

        if self.config.only_if_missing and response.headers.get("cache-control"):
            return response

        path = request.url.path
        cc = (
            _longest_prefix_match(path, self._def.path_overrides)
            or self._def.default_cache_control
        )
        response.headers["Cache-Control"] = cc

        if self.config.set_cdn_headers:
            if self._def.cdn_cache_control:
                response.headers.setdefault(
                    "CDN-Cache-Control", self._def.cdn_cache_control
                )
            if self._def.surrogate_control:
                response.headers.setdefault(
                    "Surrogate-Control", self._def.surrogate_control
                )

        if self._def.vary and not response.headers.get("vary"):
            response.headers["Vary"] = self._def.vary

        return response


__all__ = [
    "EdgePerformanceTier",
    "EdgeTierCacheHeadersConfig",
    "EdgeTierCacheHeadersMiddleware",
    "EdgeTierDefinition",
    "tier_definition",
]
