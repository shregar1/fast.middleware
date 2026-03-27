"""Tests for Request Context middleware."""

import pytest
from fastapi import FastAPI, Request
from starlette.testclient import TestClient

from fastmiddleware import (
    RequestContextMiddleware,
    get_request_context,
    get_request_id,
)


@pytest.fixture
def context_app() -> FastAPI:
    """Create app with request context middleware."""
    app = FastAPI()
    app.add_middleware(RequestContextMiddleware)

    @app.get("/")
    async def root(request: Request):
        """Execute root operation.

        Args:
            request: The request parameter.

        Returns:
            The result of the operation.
        """
        return {
            "request_id": request.state.request_id,
            "has_start_time": request.state.start_time is not None,
        }

    @app.get("/context-var")
    async def context_var():
        """Execute context_var operation.

        Returns:
            The result of the operation.
        """
        return {
            "request_id": get_request_id(),
            "context": get_request_context(),
        }

    return app


@pytest.fixture
def context_client(context_app: FastAPI) -> TestClient:
    """Create test client for context app."""
    return TestClient(context_app)


class TestRequestContextMiddleware:
    """Tests for RequestContextMiddleware."""

    def test_request_id_in_state(self, context_client: TestClient):
        """Test that request ID is added to request.state."""
        response = context_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["request_id"] is not None
        assert len(data["request_id"]) > 0

    def test_start_time_in_state(self, context_client: TestClient):
        """Test that start time is added to request.state."""
        response = context_client.get("/")

        assert response.status_code == 200
        assert response.json()["has_start_time"] is True

    def test_response_headers(self, context_client: TestClient):
        """Test that response headers are added."""
        response = context_client.get("/")

        assert "X-Request-ID" in response.headers
        assert "X-Process-Time" in response.headers

    def test_trusts_incoming_request_id(self, context_client: TestClient):
        """Test that incoming request IDs are trusted."""
        custom_id = "my-custom-id"
        response = context_client.get("/", headers={"X-Request-ID": custom_id})

        assert response.headers["X-Request-ID"] == custom_id
        assert response.json()["request_id"] == custom_id


class TestContextVariables:
    """Tests for context variable functions."""

    def test_get_request_id(self, context_client: TestClient):
        """Test get_request_id function."""
        response = context_client.get("/context-var")

        assert response.status_code == 200
        data = response.json()
        assert data["request_id"] is not None

    def test_get_request_context(self, context_client: TestClient):
        """Test get_request_context function."""
        response = context_client.get("/context-var")

        assert response.status_code == 200
        ctx = response.json()["context"]

        assert "request_id" in ctx
        assert "client_ip" in ctx
        assert "method" in ctx
        assert "path" in ctx
        assert ctx["method"] == "GET"
        assert ctx["path"] == "/context-var"

    def test_context_variables_isolated(self, context_client: TestClient):
        """Test that context variables are isolated per request."""
        response1 = context_client.get("/context-var")
        response2 = context_client.get("/context-var")

        id1 = response1.json()["request_id"]
        id2 = response2.json()["request_id"]

        assert id1 != id2


class TestContextCustomConfiguration:
    """Tests for custom context configuration."""

    @pytest.fixture
    def custom_context_app(self) -> FastAPI:
        """Create app with custom context configuration."""
        app = FastAPI()

        counter = {"value": 0}

        def custom_generator():
            """Execute custom_generator operation.

            Returns:
                The result of the operation.
            """
            counter["value"] += 1
            return f"ctx-{counter['value']}"

        app.add_middleware(
            RequestContextMiddleware,
            id_generator=custom_generator,
            request_id_header="X-Correlation-ID",
            process_time_header="X-Duration",
            trust_incoming_id=False,
        )

        @app.get("/")
        async def root(request: Request):
            """Execute root operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return {"request_id": request.state.request_id}

        return app

    @pytest.fixture
    def custom_context_client(self, custom_context_app: FastAPI) -> TestClient:
        """Create test client for custom context app."""
        return TestClient(custom_context_app)

    def test_custom_generator(self, custom_context_client: TestClient):
        """Test custom ID generator."""
        response = custom_context_client.get("/")

        assert response.json()["request_id"].startswith("ctx-")

    def test_custom_headers(self, custom_context_client: TestClient):
        """Test custom header names."""
        response = custom_context_client.get("/")

        assert "X-Correlation-ID" in response.headers
        assert "X-Duration" in response.headers
        assert "X-Request-ID" not in response.headers
        assert "X-Process-Time" not in response.headers

    def test_ignores_incoming_when_disabled(self, custom_context_client: TestClient):
        """Test that incoming IDs are ignored when trust is disabled."""
        response = custom_context_client.get(
            "/", headers={"X-Correlation-ID": "should-be-ignored"}
        )

        assert response.json()["request_id"].startswith("ctx-")
