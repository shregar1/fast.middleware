"""Tests for CORS middleware."""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import CORSMiddleware


@pytest.fixture
def cors_app(sample_routes) -> FastAPI:
    """Create app with CORS middleware."""
    app = sample_routes
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://example.com"],
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    return app


@pytest.fixture
def cors_client(cors_app: FastAPI) -> TestClient:
    """Create test client for CORS app."""
    return TestClient(cors_app)


class TestCORSMiddleware:
    """Tests for CORSMiddleware."""

    def test_cors_headers_on_valid_origin(self, cors_client: TestClient):
        """Test that CORS headers are added for valid origins."""
        response = cors_client.get("/", headers={"Origin": "https://example.com"})
        assert response.status_code == 200
        assert (
            response.headers.get("access-control-allow-origin") == "https://example.com"
        )
        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_cors_preflight_request(self, cors_client: TestClient):
        """Test preflight OPTIONS request."""
        response = cors_client.options(
            "/",
            headers={
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-methods" in response.headers

    def test_cors_invalid_origin(self, cors_client: TestClient):
        """Test that invalid origins don't get CORS headers."""
        response = cors_client.get("/", headers={"Origin": "https://malicious.com"})
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") is None


class TestCORSWildcard:
    """Tests for wildcard CORS configuration."""

    @pytest.fixture
    def wildcard_app(self, sample_routes) -> FastAPI:
        """Create app with wildcard CORS."""
        app = sample_routes
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
        )
        return app

    @pytest.fixture
    def wildcard_client(self, wildcard_app: FastAPI) -> TestClient:
        """Create test client for wildcard CORS app."""
        return TestClient(wildcard_app)

    def test_wildcard_allows_any_origin(self, wildcard_client: TestClient):
        """Test that wildcard allows any origin."""
        response = wildcard_client.get(
            "/", headers={"Origin": "https://any-domain.com"}
        )
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == "*"
