"""Content Type Validation Middleware for FastMVC.

Validates Content-Type headers on incoming requests.
"""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from fastx_middleware.mw_core.base import FastMVCMiddleware
from fastx_middleware.constants import *


@dataclass
class ContentTypeConfig:
    """Configuration for content type validation middleware.

    Attributes:
        allowed_types: Allowed content types for each method.
        default_allowed: Default allowed types if method not specified.
        strict: Reject requests without Content-Type header.
        methods_requiring_body: Methods that require Content-Type.

    Example:
        ```python
        from fastmiddleware import ContentTypeConfig

        config = ContentTypeConfig(
            allowed_types={
                "POST": {CONTENT_TYPE_JSON, CONTENT_TYPE_MULTIPART},
                "PUT": {CONTENT_TYPE_JSON},
                "PATCH": {CONTENT_TYPE_JSON},
            },
        )
        ```

    """

    allowed_types: dict[str, set[str]] = field(default_factory=dict)
    default_allowed: set[str] = field(
        default_factory=lambda: {
            CONTENT_TYPE_JSON,
            CONTENT_TYPE_FORM_URLENCODED,
            CONTENT_TYPE_MULTIPART,
        }
    )
    strict: bool = False
    methods_requiring_body: set[str] = field(
        default_factory=lambda: {"POST", "PUT", "PATCH"}
    )


class ContentTypeMiddleware(FastMVCMiddleware):
    """Middleware that validates Content-Type headers.

    Ensures requests have appropriate Content-Type headers for
    methods that include request bodies.

    Features:
        - Per-method allowed content types
        - Strict mode (require Content-Type)
        - Automatic JSON enforcement

    Example:
        ```python
        from fastapi import FastAPI
        from fastmiddleware import ContentTypeMiddleware

        app = FastAPI()

        # Basic - require JSON for body methods
        app.add_middleware(
            ContentTypeMiddleware,
            strict=True,
        )

        # Custom allowed types
        app.add_middleware(
            ContentTypeMiddleware,
            allowed_types={
                "POST": {CONTENT_TYPE_JSON},
                "PUT": {CONTENT_TYPE_JSON},
            },
        )
        ```

    """

    def __init__(
        self,
        app,
        config: ContentTypeConfig | None = None,
        allowed_types: dict[str, set[str]] | None = None,
        strict: bool | None = None,
        exclude_paths: set[str] | None = None,
    ) -> None:
        """Initialize the content type middleware.

        Args:
            app: The ASGI application.
            config: Content type configuration.
            allowed_types: Per-method allowed types (overrides config).
            strict: Strict mode (overrides config).
            exclude_paths: Paths to exclude.

        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.config = config or ContentTypeConfig()

        if allowed_types is not None:
            self.config.allowed_types = allowed_types
        if strict is not None:
            self.config.strict = strict

    def _get_allowed_types(self, method: str) -> set[str]:
        """Get allowed content types for method."""
        return self.config.allowed_types.get(
            method.upper(), self.config.default_allowed
        )

    def _extract_content_type(self, content_type: str) -> str:
        """Extract base content type (remove charset, etc.)."""
        if not content_type:
            return ""
        return content_type.split(";")[0].strip().lower()

    def _requires_body(self, request: Request) -> bool:
        """Check if method typically requires a body."""
        return request.method.upper() in self.config.methods_requiring_body

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request with content type validation.

        Args:
            request: The incoming HTTP request.
            call_next: Callable to invoke the next middleware.

        Returns:
            The response or 415 if content type invalid.

        """
        if self.should_skip(request):
            return await call_next(request)

        # Only check methods that require a body
        if not self._requires_body(request):
            return await call_next(request)

        content_type = request.headers.get(HEADER_CONTENT_TYPE, "")
        base_type = self._extract_content_type(content_type)

        # Check if Content-Type is required
        if not base_type:
            if self.config.strict:
                return JSONResponse(
                    status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    content={
                        FIELD_ERROR: True,
                        FIELD_MESSAGE: "Content-Type header is required",
                    },
                )
            # Not strict, allow
            return await call_next(request)

        # Validate content type
        allowed = self._get_allowed_types(request.method)
        if base_type not in allowed:
            return JSONResponse(
                status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                content={
                    FIELD_ERROR: True,
                    FIELD_MESSAGE: f"Unsupported Content-Type: {base_type}",
                    "allowed": list(allowed),
                },
            )

        return await call_next(request)
