"""Custom middleware example for FastMVC Middleware.

This example demonstrates how to create your own middleware
by extending FastMVCMiddleware base class.

Run with: uvicorn examples.custom_middleware:app --reload
"""

import time
from typing import Set, Dict, Any

from fastapi import FastAPI, Request
from starlette.responses import Response, JSONResponse

from fastmiddleware import FastMVCMiddleware, get_request_id


# ============================================================================
# Custom Middleware Examples
# ============================================================================


class MaintenanceModeMiddleware(FastMVCMiddleware):
    """Middleware that enables maintenance mode.

    When enabled, all requests (except excluded paths) return a 503 response.
    """

    def __init__(
        self,
        app,
        enabled: bool = False,
        message: str = "Service temporarily unavailable for maintenance",
        exclude_paths: Set[str] | None = None,
        exclude_methods: Set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            enabled: The enabled parameter.
            message: The message parameter.
            exclude_paths: The exclude_paths parameter.
            exclude_methods: The exclude_methods parameter.
        """
        super().__init__(
            app, exclude_paths=exclude_paths, exclude_methods=exclude_methods
        )
        self.enabled = enabled
        self.message = message

    async def dispatch(self, request: Request, call_next) -> Response:
        """Execute dispatch operation.

        Args:
            request: The request parameter.
            call_next: The call_next parameter.

        Returns:
            The result of the operation.
        """
        # Skip if maintenance mode is disabled
        if not self.enabled:
            return await call_next(request)

        # Skip excluded paths (health checks, etc.)
        if self.should_skip(request):
            return await call_next(request)

        # Return maintenance response
        return JSONResponse(
            content={
                "detail": self.message,
                "maintenance": True,
            },
            status_code=503,
            headers={"Retry-After": "300"},
        )


class GeoIPMiddleware(FastMVCMiddleware):
    """Middleware that adds geographic information based on client IP.

    In production, you would integrate with a GeoIP database like MaxMind.
    This example uses mock data for demonstration.
    """

    # Mock GeoIP data (in production, use a real GeoIP database)
    MOCK_GEO_DATA: Dict[str, Dict[str, Any]] = {
        "127.0.0.1": {"country": "Local", "city": "Localhost", "timezone": "UTC"},
        "testclient": {"country": "Test", "city": "TestCity", "timezone": "UTC"},
    }

    def __init__(
        self,
        app,
        default_country: str = "Unknown",
        exclude_paths: Set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            default_country: The default_country parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.default_country = default_country

    async def dispatch(self, request: Request, call_next) -> Response:
        """Execute dispatch operation.

        Args:
            request: The request parameter.
            call_next: The call_next parameter.

        Returns:
            The result of the operation.
        """
        # Get client IP
        client_ip = self.get_client_ip(request)

        # Look up geographic data
        geo_data = self.MOCK_GEO_DATA.get(
            client_ip,
            {
                "country": self.default_country,
                "city": "Unknown",
                "timezone": "UTC",
            },
        )

        # Store in request state
        request.state.geo = geo_data
        request.state.country = geo_data.get("country")

        return await call_next(request)


class RequestThrottleMiddleware(FastMVCMiddleware):
    """Middleware that adds artificial delay to requests.

    Useful for testing slow network conditions or simulating
    high-latency services.
    """

    def __init__(
        self,
        app,
        delay_seconds: float = 0.0,
        delay_paths: Set[str] | None = None,
        exclude_paths: Set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            delay_seconds: The delay_seconds parameter.
            delay_paths: The delay_paths parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.delay_seconds = delay_seconds
        self.delay_paths = delay_paths or set()

    async def dispatch(self, request: Request, call_next) -> Response:
        """Execute dispatch operation.

        Args:
            request: The request parameter.
            call_next: The call_next parameter.

        Returns:
            The result of the operation.
        """
        import asyncio

        # Skip if no delay configured
        if self.delay_seconds <= 0:
            return await call_next(request)

        # Skip excluded paths
        if self.should_skip(request):
            return await call_next(request)

        # Only delay specific paths if configured
        if self.delay_paths and request.url.path not in self.delay_paths:
            return await call_next(request)

        # Add delay
        await asyncio.sleep(self.delay_seconds)

        response = await call_next(request)
        response.headers["X-Artificial-Delay"] = f"{self.delay_seconds}s"

        return response


class DeprecationWarningMiddleware(FastMVCMiddleware):
    """Middleware that adds deprecation warnings to specific endpoints.

    Useful for notifying clients about upcoming API changes.
    """

    def __init__(
        self,
        app,
        deprecated_paths: Dict[str, str] | None = None,
        exclude_paths: Set[str] | None = None,
    ) -> None:
        """Execute __init__ operation.

        Args:
            app: The app parameter.
            deprecated_paths: The deprecated_paths parameter.
            exclude_paths: The exclude_paths parameter.
        """
        super().__init__(app, exclude_paths=exclude_paths)
        self.deprecated_paths = deprecated_paths or {}

    async def dispatch(self, request: Request, call_next) -> Response:
        """Execute dispatch operation.

        Args:
            request: The request parameter.
            call_next: The call_next parameter.

        Returns:
            The result of the operation.
        """
        response = await call_next(request)

        # Check if path is deprecated
        if request.url.path in self.deprecated_paths:
            message = self.deprecated_paths[request.url.path]
            response.headers["Deprecation"] = "true"
            response.headers["Sunset"] = message
            response.headers["X-Deprecation-Notice"] = message

        return response


# ============================================================================
# Application Setup
# ============================================================================

app = FastAPI(
    title="Custom Middleware Example",
    description="Demonstrates creating custom middleware",
    version="1.0.0",
)

# Add custom middleware
app.add_middleware(
    DeprecationWarningMiddleware,
    deprecated_paths={
        "/v1/old-endpoint": "This endpoint will be removed on 2026-06-01. Use /v2/new-endpoint instead.",
    },
)

app.add_middleware(
    RequestThrottleMiddleware,
    delay_seconds=0.0,  # Set to > 0 to enable throttling
)

app.add_middleware(GeoIPMiddleware)

app.add_middleware(
    MaintenanceModeMiddleware,
    enabled=False,  # Set to True to enable maintenance mode
    exclude_paths={"/health"},
)


# ============================================================================
# Routes
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Custom Middleware Example"}


@app.get("/health")
async def health():
    """Health check (works even in maintenance mode)."""
    return {"status": "healthy"}


@app.get("/geo")
async def geo_info(request: Request):
    """Shows geographic information from middleware."""
    return {
        "geo": getattr(request.state, "geo", None),
        "country": getattr(request.state, "country", None),
        "client_ip": request.client.host if request.client else None,
    }


@app.get("/v1/old-endpoint")
async def deprecated_endpoint():
    """Deprecated endpoint that shows deprecation warnings."""
    return {"data": "This is old data", "version": "v1"}


@app.get("/v2/new-endpoint")
async def new_endpoint():
    """New endpoint replacing the deprecated one."""
    return {"data": "This is new data", "version": "v2"}


@app.get("/slow")
async def slow_endpoint():
    """Endpoint for testing throttle middleware."""
    return {"message": "This might be slow if throttling is enabled"}


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("Starting custom middleware example...")
    print("Try these endpoints:")
    print("  GET /geo - Shows geographic info")
    print("  GET /v1/old-endpoint - Shows deprecation warnings")
    print("  GET /v2/new-endpoint - No deprecation warnings")

    uvicorn.run(app, host="0.0.0.0", port=8000)
