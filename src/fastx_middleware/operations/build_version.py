"""Expose application build/version metadata on every response (support & observability)."""

from __future__ import annotations

import os
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

from starlette.requests import Request
from starlette.responses import Response

from fastx_middleware.mw_core.base import FastMVCMiddleware

_DEFAULT_ENV_VERSION = "APP_VERSION"
_DEFAULT_ENV_GIT = "GIT_SHA"


@dataclass
class BuildVersionConfig:
    """Response headers for release/version metadata.

    If ``version`` / ``git_sha`` are unset, values are read from the environment
    (see ``version_env`` / ``git_sha_env``). Empty strings are skipped unless
    ``include_empty`` is True.
    """

    version: str | None = None
    version_header: str = "X-App-Version"
    version_env: str = _DEFAULT_ENV_VERSION

    git_sha: str | None = None
    git_sha_header: str = "X-Git-SHA"
    git_sha_env: str = _DEFAULT_ENV_GIT

    include_empty: bool = False


class BuildVersionMiddleware(FastMVCMiddleware):
    """Add ``X-App-Version`` / ``X-Git-SHA`` (or custom names) to responses.

    Typical env wiring::

        export APP_VERSION=2.4.1
        export GIT_SHA=$(git rev-parse --short HEAD)

    Example::

        from fastmiddleware import BuildVersionMiddleware, BuildVersionConfig

        app.add_middleware(
            BuildVersionMiddleware,
            config=BuildVersionConfig(version_header="X-Release", git_sha_header="X-Commit"),
        )
    """

    def __init__(
        self,
        app,
        config: BuildVersionConfig | None = None,
        *,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or BuildVersionConfig()
        self._version = self._resolve_version()
        self._git = self._resolve_git()

    def _resolve_version(self) -> str | None:
        """Execute _resolve_version operation.

        Returns:
            The result of the operation.
        """
        if self.config.version is not None:
            v = self.config.version.strip()
        else:
            raw = os.environ.get(self.config.version_env, "")
            v = raw.strip() if raw else ""
        if not v and not self.config.include_empty:
            return None
        return v or None

    def _resolve_git(self) -> str | None:
        """Execute _resolve_git operation.

        Returns:
            The result of the operation.
        """
        if self.config.git_sha is not None:
            g = self.config.git_sha.strip()
        else:
            raw = os.environ.get(self.config.git_sha_env, "")
            g = raw.strip() if raw else ""
        if not g and not self.config.include_empty:
            return None
        return g or None

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

        if self._version is not None:
            response.headers[self.config.version_header] = self._version
        if self._git is not None:
            response.headers[self.config.git_sha_header] = self._git

        return response
