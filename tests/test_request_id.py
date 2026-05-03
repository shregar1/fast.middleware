"""Tests for Request ID middleware."""

import uuid

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import RequestIDMiddleware


@pytest.fixture
def request_id_app(sample_routes) -> FastAPI:
    """Create app with request ID middleware."""
    app = sample_routes
    app.add_middleware(RequestIDMiddleware)
    return app


@pytest.fixture
def request_id_client(request_id_app: FastAPI) -> TestClient:
    """Create test client for request ID app."""
    return TestClient(request_id_app)


class TestRequestIDMiddleware:
    """Tests for RequestIDMiddleware."""

    def test_request_id_header_added(self, request_id_client: TestClient):
        """Test that X-Request-ID header is added to response."""
        response = request_id_client.get("/")

        assert response.status_code == 200
        assert "X-Request-ID" in response.headers

    def test_request_id_is_valid_uuid(self, request_id_client: TestClient):
        """Test that request ID is a valid UUID."""
        response = request_id_client.get("/")
        request_id = response.headers["X-Request-ID"]

        # Should not raise an exception
        uuid.UUID(request_id)

    def test_request_id_unique_per_request(self, request_id_client: TestClient):
        """Test that each request gets a unique ID."""
        response1 = request_id_client.get("/")
        response2 = request_id_client.get("/")

        id1 = response1.headers["X-Request-ID"]
        id2 = response2.headers["X-Request-ID"]

        assert id1 != id2

    def test_trusts_incoming_request_id(self, request_id_client: TestClient):
        """Test that incoming request IDs are trusted and reused."""
        custom_id = "custom-request-id-12345"
        response = request_id_client.get("/", headers={"X-Request-ID": custom_id})

        assert response.headers["X-Request-ID"] == custom_id


class TestRequestIDCustomGenerator:
    """Tests for custom request ID generator."""

    @pytest.fixture
    def custom_gen_app(self, sample_routes) -> FastAPI:
        """Create app with custom ID generator."""
        counter = {"value": 0}

        def custom_generator():
            """Execute custom_generator operation.

            Returns:
                The result of the operation.
            """
            counter["value"] += 1
            return f"req-{counter['value']:05d}"

        app = sample_routes
        app.add_middleware(
            RequestIDMiddleware,
            id_factory=custom_generator,
            accept_incoming=False,
        )
        return app

    @pytest.fixture
    def custom_gen_client(self, custom_gen_app: FastAPI) -> TestClient:
        """Create test client for custom generator app."""
        return TestClient(custom_gen_app)

    def test_custom_generator_used(self, custom_gen_client: TestClient):
        """Test that custom generator is used."""
        response = custom_gen_client.get("/")
        request_id = response.headers["X-Request-ID"]

        assert request_id.startswith("req-")

    def test_ignores_incoming_when_trust_disabled(self, custom_gen_client: TestClient):
        """Test that incoming IDs are ignored when trust is disabled."""
        response = custom_gen_client.get(
            "/", headers={"X-Request-ID": "should-be-ignored"}
        )

        assert response.headers["X-Request-ID"].startswith("req-")


class TestRequestIDCustomHeader:
    """Tests for custom header name."""

    @pytest.fixture
    def custom_header_app(self, sample_routes) -> FastAPI:
        """Create app with custom header name."""
        app = sample_routes
        app.add_middleware(
            RequestIDMiddleware,
            header_name="X-Correlation-ID",
        )
        return app

    @pytest.fixture
    def custom_header_client(self, custom_header_app: FastAPI) -> TestClient:
        """Create test client for custom header app."""
        return TestClient(custom_header_app)

    def test_custom_header_name(self, custom_header_client: TestClient):
        """Test that custom header name is used."""
        response = custom_header_client.get("/")

        assert "X-Correlation-ID" in response.headers
        assert "X-Request-ID" not in response.headers
