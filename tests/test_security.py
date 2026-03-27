"""Tests for Security Headers middleware."""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import SecurityHeadersConfig, SecurityHeadersMiddleware


@pytest.fixture
def security_app(sample_routes) -> FastAPI:
    """Create app with security middleware."""
    app = sample_routes
    app.add_middleware(SecurityHeadersMiddleware)
    return app


@pytest.fixture
def security_client(security_app: FastAPI) -> TestClient:
    """Create test client for security app."""
    return TestClient(security_app)


class TestSecurityHeadersMiddleware:
    """Tests for SecurityHeadersMiddleware."""

    def test_default_security_headers(self, security_client: TestClient):
        """Test that default security headers are added."""
        response = security_client.get("/")

        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert (
            response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        )
        assert "Content-Security-Policy" in response.headers
        assert "Permissions-Policy" in response.headers

    def test_hsts_disabled_by_default(self, security_client: TestClient):
        """Test that HSTS is disabled by default."""
        response = security_client.get("/")
        assert "Strict-Transport-Security" not in response.headers


class TestSecurityHeadersWithHSTS:
    """Tests for security headers with HSTS enabled."""

    @pytest.fixture
    def hsts_app(self, sample_routes) -> FastAPI:
        """Create app with HSTS enabled."""
        app = sample_routes
        app.add_middleware(
            SecurityHeadersMiddleware,
            enable_hsts=True,
            hsts_max_age=31536000,
            hsts_include_subdomains=True,
            hsts_preload=True,
        )
        return app

    @pytest.fixture
    def hsts_client(self, hsts_app: FastAPI) -> TestClient:
        """Create test client for HSTS app."""
        return TestClient(hsts_app)

    def test_hsts_header_added(self, hsts_client: TestClient):
        """Test that HSTS header is added when enabled."""
        response = hsts_client.get("/")
        hsts = response.headers.get("Strict-Transport-Security")

        assert hsts is not None
        assert "max-age=31536000" in hsts
        assert "includeSubDomains" in hsts
        assert "preload" in hsts


class TestSecurityHeadersConfig:
    """Tests for SecurityHeadersConfig."""

    def test_config_object(self, sample_routes):
        """Test using configuration object."""
        config = SecurityHeadersConfig(
            x_frame_options="SAMEORIGIN",
            enable_hsts=True,
            content_security_policy="default-src 'self'",
        )

        app = sample_routes
        app.add_middleware(SecurityHeadersMiddleware, config=config)
        client = TestClient(app)

        response = client.get("/")
        assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
        assert response.headers.get("Content-Security-Policy") == "default-src 'self'"
        assert "Strict-Transport-Security" in response.headers

    def test_build_hsts_header(self):
        """Test HSTS header building."""
        config = SecurityHeadersConfig(
            hsts_max_age=3600,
            hsts_include_subdomains=True,
            hsts_preload=False,
        )

        hsts = config.build_hsts_header()
        assert hsts == "max-age=3600; includeSubDomains"
