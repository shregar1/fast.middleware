"""Section layout for :mod:`fastmiddleware` (aligned with ``fastx_platform.taxonomy``).

- **mw_core** — factory, CORS, logging, timing, body limits, client IP, request id, compression
  (named ``mw_core`` to avoid clashing with ``core.*`` from ``fast-platform`` on ``PYTHONPATH``).
- **sec** — security headers, CSRF, auth backends, JWT bearer, webhooks, etc.
- **operations** — rate limits, metrics, health, sessions, caching, i18n, routing helpers,
  build/version headers, immutable static ``Cache-Control``, DNS prefetch control,
  edge performance tiers (feed / creator / live CDN cache semantics), etc.
"""

from __future__ import annotations

from enum import Enum
from typing import Final

__all__ = ["MiddlewareSection", "SECTION_SUBPACKAGES"]


class MiddlewareSection(str, Enum):
    """Represents the MiddlewareSection class."""

    MW_CORE = "mw_core"
    SECURITY = "sec"
    OPERATIONS = "operations"


SECTION_SUBPACKAGES: Final[dict[MiddlewareSection, str]] = {
    MiddlewareSection.MW_CORE: "mw_core",
    MiddlewareSection.SECURITY: "sec",
    MiddlewareSection.OPERATIONS: "operations",
}
