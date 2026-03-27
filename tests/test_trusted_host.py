"""Comprehensive tests for Trusted Host middleware."""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import TrustedHostMiddleware


@pytest.fixture
def sample_app() -> FastAPI:
    """Create a sample FastAPI app."""
    app = FastAPI()

    @app.get("/")
    async def root():
        """Execute root operation.

        Returns:
            The result of the operation.
        """
        return {"message": "Hello"}

    @app.get("/health")
    async def health():
        """Execute health operation.

        Returns:
            The result of the operation.
        """
        return {"status": "ok"}

    return app


class TestTrustedHostMiddleware:
    """Tests for TrustedHostMiddleware."""

    @pytest.fixture
    def trusted_host_app(self, sample_app) -> FastAPI:
        """Create app with trusted host middleware."""
        sample_app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["example.com", "www.example.com"],
        )
        return sample_app

    @pytest.fixture
    def trusted_host_client(self, trusted_host_app: FastAPI) -> TestClient:
        """Execute trusted_host_client operation.

        Args:
            trusted_host_app: The trusted_host_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(trusted_host_app)

    def test_valid_host_allowed(self, trusted_host_client: TestClient):
        """Test that valid host is allowed."""
        response = trusted_host_client.get("/", headers={"Host": "example.com"})
        assert response.status_code == 200
        assert response.json() == {"message": "Hello"}

    def test_valid_www_host_allowed(self, trusted_host_client: TestClient):
        """Test that www subdomain is allowed."""
        response = trusted_host_client.get("/", headers={"Host": "www.example.com"})
        assert response.status_code == 200

    def test_invalid_host_rejected(self, trusted_host_client: TestClient):
        """Test that invalid host is rejected."""
        response = trusted_host_client.get("/", headers={"Host": "malicious.com"})
        assert response.status_code == 400
        assert "Invalid host" in response.text

    def test_host_with_port_allowed(self, trusted_host_client: TestClient):
        """Test that host with port is allowed."""
        response = trusted_host_client.get("/", headers={"Host": "example.com:8000"})
        assert response.status_code == 200

    def test_case_insensitive_matching(self, trusted_host_client: TestClient):
        """Test that host matching is case insensitive."""
        response = trusted_host_client.get("/", headers={"Host": "EXAMPLE.COM"})
        assert response.status_code == 200


class TestWildcardHost:
    """Tests for wildcard host matching."""

    @pytest.fixture
    def wildcard_app(self, sample_app) -> FastAPI:
        """Create app with wildcard host pattern."""
        sample_app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*.example.com"],
        )
        return sample_app

    @pytest.fixture
    def wildcard_client(self, wildcard_app: FastAPI) -> TestClient:
        """Execute wildcard_client operation.

        Args:
            wildcard_app: The wildcard_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(wildcard_app)

    def test_subdomain_allowed(self, wildcard_client: TestClient):
        """Test that subdomains are allowed."""
        response = wildcard_client.get("/", headers={"Host": "api.example.com"})
        assert response.status_code == 200

    def test_nested_subdomain_allowed(self, wildcard_client: TestClient):
        """Test that nested subdomains are allowed."""
        response = wildcard_client.get("/", headers={"Host": "staging.api.example.com"})
        assert response.status_code == 200

    def test_different_domain_rejected(self, wildcard_client: TestClient):
        """Test that different domains are rejected."""
        response = wildcard_client.get("/", headers={"Host": "example.org"})
        assert response.status_code == 400


class TestAllowAnyHost:
    """Tests for allowing any host."""

    @pytest.fixture
    def any_host_app(self, sample_app) -> FastAPI:
        """Create app allowing any host."""
        sample_app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"],
        )
        return sample_app

    @pytest.fixture
    def any_host_client(self, any_host_app: FastAPI) -> TestClient:
        """Execute any_host_client operation.

        Args:
            any_host_app: The any_host_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(any_host_app)

    def test_any_host_allowed(self, any_host_client: TestClient):
        """Test that any host is allowed with wildcard."""
        response = any_host_client.get("/", headers={"Host": "anything.example.org"})
        assert response.status_code == 200

    def test_localhost_allowed(self, any_host_client: TestClient):
        """Test that localhost is allowed."""
        response = any_host_client.get("/", headers={"Host": "localhost:8000"})
        assert response.status_code == 200


class TestMixedHosts:
    """Tests for mixed host patterns."""

    @pytest.fixture
    def mixed_app(self, sample_app) -> FastAPI:
        """Create app with mixed host patterns."""
        sample_app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["example.com", "*.staging.example.com", "localhost"],
        )
        return sample_app

    @pytest.fixture
    def mixed_client(self, mixed_app: FastAPI) -> TestClient:
        """Execute mixed_client operation.

        Args:
            mixed_app: The mixed_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(mixed_app)

    def test_exact_match_allowed(self, mixed_client: TestClient):
        """Test exact host match."""
        response = mixed_client.get("/", headers={"Host": "example.com"})
        assert response.status_code == 200

    def test_wildcard_match_allowed(self, mixed_client: TestClient):
        """Test wildcard host match."""
        response = mixed_client.get("/", headers={"Host": "api.staging.example.com"})
        assert response.status_code == 200

    def test_localhost_allowed(self, mixed_client: TestClient):
        """Test localhost match."""
        response = mixed_client.get("/", headers={"Host": "localhost"})
        assert response.status_code == 200

    def test_unmatched_rejected(self, mixed_client: TestClient):
        """Test unmatched host is rejected."""
        response = mixed_client.get("/", headers={"Host": "production.example.com"})
        assert response.status_code == 400


class TestPathExclusion:
    """Tests for path exclusion."""

    @pytest.fixture
    def excluded_app(self, sample_app) -> FastAPI:
        """Create app with path exclusion."""
        sample_app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["example.com"],
            exclude_paths={"/health"},
        )
        return sample_app

    @pytest.fixture
    def excluded_client(self, excluded_app: FastAPI) -> TestClient:
        """Execute excluded_client operation.

        Args:
            excluded_app: The excluded_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(excluded_app)

    def test_excluded_path_allows_any_host(self, excluded_client: TestClient):
        """Test that excluded paths allow any host."""
        response = excluded_client.get("/health", headers={"Host": "malicious.com"})
        assert response.status_code == 200

    def test_non_excluded_path_validates_host(self, excluded_client: TestClient):
        """Test that non-excluded paths validate host."""
        response = excluded_client.get("/", headers={"Host": "malicious.com"})
        assert response.status_code == 400


class TestEmptyHost:
    """Tests for empty or missing host header."""

    @pytest.fixture
    def app(self, sample_app) -> FastAPI:
        """Execute app operation.

        Args:
            sample_app: The sample_app parameter.

        Returns:
            The result of the operation.
        """
        sample_app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["example.com"],
        )
        return sample_app

    @pytest.fixture
    def client(self, app: FastAPI) -> TestClient:
        """Execute client operation.

        Args:
            app: The app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(app)

    def test_empty_host_rejected(self, client: TestClient):
        """Test that empty host is rejected."""
        response = client.get("/", headers={"Host": ""})
        assert response.status_code == 400
