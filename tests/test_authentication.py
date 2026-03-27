"""Tests for Authentication middleware."""

import pytest
from fastapi import FastAPI, Request
from starlette.testclient import TestClient

from fastmiddleware import (
    APIKeyAuthBackend,
    AuthConfig,
    AuthenticationMiddleware,
)


class TestAPIKeyAuthBackend:
    """Tests for API Key authentication backend."""

    @pytest.fixture
    def static_keys_backend(self):
        """Create backend with static keys."""
        return APIKeyAuthBackend(valid_keys={"key1", "key2", "key3"})

    @pytest.mark.asyncio
    async def test_valid_key_authenticates(self, static_keys_backend):
        """Test that valid API key authenticates successfully."""
        result = await static_keys_backend.authenticate(None, "key1")

        assert result is not None
        assert result["api_key"] == "key1"

    @pytest.mark.asyncio
    async def test_invalid_key_fails(self, static_keys_backend):
        """Test that invalid API key fails authentication."""
        result = await static_keys_backend.authenticate(None, "invalid")

        assert result is None

    @pytest.mark.asyncio
    async def test_custom_validator(self):
        """Test custom validator function."""

        async def validator(key: str):
            """Execute validator operation.

            Args:
                key: The key parameter.

            Returns:
                The result of the operation.
            """
            if key == "special-key":
                return {"user_id": 123, "tier": "premium"}
            return None

        backend = APIKeyAuthBackend(validator=validator)
        result = await backend.authenticate(None, "special-key")

        assert result is not None
        assert result["user_id"] == 123
        assert result["tier"] == "premium"

    def test_requires_keys_or_validator(self):
        """Test that either valid_keys or validator must be provided."""
        with pytest.raises(ValueError):
            APIKeyAuthBackend()


class TestAuthenticationMiddleware:
    """Tests for AuthenticationMiddleware."""

    @pytest.fixture
    def auth_app(self, sample_routes) -> FastAPI:
        """Create app with authentication middleware."""
        app = sample_routes
        backend = APIKeyAuthBackend(valid_keys={"test-api-key"})
        config = AuthConfig(
            exclude_paths={"/health", "/"},
        )
        app.add_middleware(
            AuthenticationMiddleware,
            backend=backend,
            config=config,
        )
        return app

    @pytest.fixture
    def auth_client(self, auth_app: FastAPI) -> TestClient:
        """Create test client for auth app."""
        return TestClient(auth_app)

    def test_excluded_path_no_auth_required(self, auth_client: TestClient):
        """Test that excluded paths don't require authentication."""
        response = auth_client.get("/health")
        assert response.status_code == 200

    def test_protected_path_requires_auth(self, auth_client: TestClient):
        """Test that protected paths require authentication."""
        response = auth_client.get("/protected")
        assert response.status_code == 401

    def test_valid_auth_succeeds(self, auth_client: TestClient):
        """Test that valid authentication succeeds."""
        response = auth_client.get(
            "/protected", headers={"Authorization": "Bearer test-api-key"}
        )
        assert response.status_code == 200

    def test_invalid_auth_fails(self, auth_client: TestClient):
        """Test that invalid authentication fails."""
        response = auth_client.get(
            "/protected", headers={"Authorization": "Bearer wrong-key"}
        )
        assert response.status_code == 401

    def test_missing_scheme_fails(self, auth_client: TestClient):
        """Test that missing auth scheme fails."""
        response = auth_client.get(
            "/protected",
            headers={"Authorization": "test-api-key"},  # No Bearer prefix
        )
        assert response.status_code == 401

    def test_auth_data_in_request_state(self):
        """Test that auth data is stored in request.state."""
        app = FastAPI()

        backend = APIKeyAuthBackend(valid_keys={"test-key"})
        app.add_middleware(
            AuthenticationMiddleware,
            backend=backend,
        )

        @app.get("/check-auth")
        async def check_auth(request: Request):
            """Execute check_auth operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return {"auth": request.state.auth}

        client = TestClient(app)
        response = client.get(
            "/check-auth", headers={"Authorization": "Bearer test-key"}
        )

        assert response.status_code == 200
        assert response.json()["auth"]["api_key"] == "test-key"


class TestAuthConfig:
    """Tests for AuthConfig."""

    def test_default_excluded_paths(self):
        """Test default excluded paths."""
        config = AuthConfig()

        assert "/health" in config.exclude_paths
        assert "/healthz" in config.exclude_paths
        assert "/docs" in config.exclude_paths
        assert "/openapi.json" in config.exclude_paths

    def test_default_excluded_methods(self):
        """Test default excluded methods."""
        config = AuthConfig()

        assert "OPTIONS" in config.exclude_methods

    def test_custom_config(self):
        """Test custom configuration."""
        config = AuthConfig(
            exclude_paths={"/custom"},
            header_name="X-API-Key",
            header_scheme="ApiKey",
            error_message="Custom error",
        )

        assert config.exclude_paths == {"/custom"}
        assert config.header_name == "X-API-Key"
        assert config.header_scheme == "ApiKey"
        assert config.error_message == "Custom error"
