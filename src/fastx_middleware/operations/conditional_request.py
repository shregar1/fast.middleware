"""Conditional Request Middleware for FastMVC.

Handles If-None-Match, If-Modified-Since, etc.
"""

import hashlib
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime, timezone

from starlette.requests import Request
from starlette.responses import Response

from fastx_middleware.mw_core.base import FastMVCMiddleware
from fastx_middleware.constants import *


@dataclass
class ConditionalRequestConfig:
    """Configuration for conditional request middleware.

    Attributes:
        weak_etag: Generate weak ETags.
        add_last_modified: Add Last-Modified header.

    """

    weak_etag: bool = True
    add_last_modified: bool = True


class ConditionalRequestMiddleware(FastMVCMiddleware):
    """Middleware for handling conditional requests.

    Handles If-None-Match and If-Modified-Since headers
    to return 304 Not Modified when appropriate.

    Example:
        ```python
        from fastmiddleware import ConditionalRequestMiddleware

        app.add_middleware(ConditionalRequestMiddleware)

        # Responses will be 304 if:
        # - If-None-Match matches ETag
        # - If-Modified-Since >= Last-Modified
        ```

    """

    def __init__(
        self,
        app,
        config: ConditionalRequestConfig | None = None,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            config: The config parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or ConditionalRequestConfig()

    def _compute_etag(self, body: bytes) -> str:
        """Compute ETag for response body."""
        hash_val = hashlib.md5(body).hexdigest()
        if self.config.weak_etag:
            return f'W/"{hash_val}"'
        return f'"{hash_val}"'

    def _etag_matches(self, request_etag: str, response_etag: str) -> bool:
        """Check if ETags match."""
        # Remove weak validator prefix for comparison
        req = request_etag.strip().lstrip("W/").strip('"')
        res = response_etag.strip().lstrip("W/").strip('"')
        return req == res

    def _parse_date(self, date_str: str) -> datetime | None:
        """Parse HTTP date."""
        formats = [
            "%a, %d %b %Y %H:%M:%S GMT",  # RFC 7231
            "%A, %d-%b-%y %H:%M:%S GMT",  # RFC 850
            "%a %b %d %H:%M:%S %Y",  # ANSI C
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        return None

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

        # Only handle GET/HEAD
        if request.method not in {"GET", "HEAD"}:
            return await call_next(request)

        response = await call_next(request)

        # Don't cache non-2xx responses
        if response.status_code < 200 or response.status_code >= 300:
            return response

        # Get response body
        if hasattr(response, "body"):
            body = response.body
        else:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            response = Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
            )

        # Compute/get ETag
        etag = response.headers.get(HEADER_ETAG)
        if not etag:
            etag = self._compute_etag(body)
            response.headers[HEADER_ETAG] = etag

        # Check If-None-Match
        if_none_match = request.headers.get(HEADER_IF_NONE_MATCH)
        if if_none_match:
            # Can be comma-separated list
            for tag in if_none_match.split(","):
                if tag.strip() == "*" or self._etag_matches(tag, etag):
                    return Response(
                        status_code=HTTP_304_NOT_MODIFIED,
                        headers={HEADER_ETAG: etag},
                    )

        # Check If-Modified-Since
        if_modified_since = request.headers.get(HEADER_IF_MODIFIED_SINCE)
        last_modified = response.headers.get(HEADER_LAST_MODIFIED)

        if if_modified_since and last_modified:
            ims = self._parse_date(if_modified_since)
            lm = self._parse_date(last_modified)

            if ims and lm and lm <= ims:
                return Response(
                    status_code=HTTP_304_NOT_MODIFIED,
                    headers={HEADER_ETAG: etag, HEADER_LAST_MODIFIED: last_modified},
                )

        return response
