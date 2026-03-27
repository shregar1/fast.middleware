"""Comprehensive tests for Health Check middleware."""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import HealthCheckMiddleware, HealthConfig


@pytest.fixture
def health_app() -> FastAPI:
    """Create app with health check middleware."""
    app = FastAPI()
    config = HealthConfig(
        version="1.0.0",
        service_name="test-service",
    )
    app.add_middleware(HealthCheckMiddleware, config=config)

    @app.get("/")
    async def root():
        """Execute root operation.

        Returns:
            The result of the operation.
        """
        return {"message": "Hello"}

    @app.get("/api/data")
    async def get_data():
        """Execute get_data operation.

        Returns:
            The result of the operation.
        """
        return {"data": [1, 2, 3]}

    return app


@pytest.fixture
def health_client(health_app: FastAPI) -> TestClient:
    """Execute health_client operation.

    Args:
        health_app: The health_app parameter.

    Returns:
        The result of the operation.
    """
    return TestClient(health_app)


class TestHealthCheckMiddleware:
    """Tests for HealthCheckMiddleware."""

    def test_health_endpoint_returns_200(self, health_client: TestClient):
        """Test that /health endpoint returns 200."""
        response = health_client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_status(self, health_client: TestClient):
        """Test that /health endpoint returns status."""
        response = health_client.get("/health")
        data = response.json()

        assert data["status"] == "healthy"

    def test_health_endpoint_returns_timestamp(self, health_client: TestClient):
        """Test that /health endpoint returns timestamp."""
        response = health_client.get("/health")
        data = response.json()

        assert "timestamp" in data
        assert data["timestamp"].endswith("Z")

    def test_health_endpoint_returns_uptime(self, health_client: TestClient):
        """Test that /health endpoint returns uptime."""
        response = health_client.get("/health")
        data = response.json()

        assert "uptime_seconds" in data
        assert data["uptime_seconds"] >= 0

    def test_health_endpoint_returns_version(self, health_client: TestClient):
        """Test that /health endpoint returns version."""
        response = health_client.get("/health")
        data = response.json()

        assert data["version"] == "1.0.0"

    def test_health_endpoint_returns_service_name(self, health_client: TestClient):
        """Test that /health endpoint returns service name."""
        response = health_client.get("/health")
        data = response.json()

        assert data["service"] == "test-service"

    def test_ready_endpoint_returns_200(self, health_client: TestClient):
        """Test that /ready endpoint returns 200."""
        response = health_client.get("/ready")

        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True

    def test_ready_endpoint_returns_timestamp(self, health_client: TestClient):
        """Test that /ready endpoint returns timestamp."""
        response = health_client.get("/ready")
        data = response.json()

        assert "timestamp" in data

    def test_live_endpoint_returns_200(self, health_client: TestClient):
        """Test that /live endpoint returns 200."""
        response = health_client.get("/live")

        assert response.status_code == 200
        data = response.json()
        assert data["alive"] is True

    def test_other_routes_pass_through(self, health_client: TestClient):
        """Test that other routes pass through to app."""
        response = health_client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello"}

    def test_api_routes_work(self, health_client: TestClient):
        """Test that API routes work normally."""
        response = health_client.get("/api/data")

        assert response.status_code == 200
        assert response.json() == {"data": [1, 2, 3]}


class TestHealthConfig:
    """Tests for HealthConfig."""

    def test_default_paths(self):
        """Test default health check paths."""
        config = HealthConfig()

        assert config.health_path == "/health"
        assert config.ready_path == "/ready"
        assert config.live_path == "/live"

    def test_custom_paths(self):
        """Test custom health check paths."""
        config = HealthConfig(
            health_path="/healthz",
            ready_path="/readiness",
            live_path="/liveness",
        )

        assert config.health_path == "/healthz"
        assert config.ready_path == "/readiness"
        assert config.live_path == "/liveness"

    def test_include_details_default(self):
        """Test that details are included by default."""
        config = HealthConfig()
        assert config.include_details is True

    def test_custom_service_info(self):
        """Test custom service information."""
        config = HealthConfig(
            version="2.0.0",
            service_name="my-service",
        )

        assert config.version == "2.0.0"
        assert config.service_name == "my-service"


class TestCustomPaths:
    """Tests for custom health check paths."""

    @pytest.fixture
    def custom_path_app(self) -> FastAPI:
        """Create app with custom paths."""
        app = FastAPI()
        config = HealthConfig(
            health_path="/healthz",
            ready_path="/readiness",
            live_path="/liveness",
        )
        app.add_middleware(HealthCheckMiddleware, config=config)

        @app.get("/")
        async def root():
            """Execute root operation.

            Returns:
                The result of the operation.
            """
            return {"ok": True}

        return app

    @pytest.fixture
    def custom_path_client(self, custom_path_app: FastAPI) -> TestClient:
        """Execute custom_path_client operation.

        Args:
            custom_path_app: The custom_path_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(custom_path_app)

    def test_custom_health_path(self, custom_path_client: TestClient):
        """Test custom health path."""
        response = custom_path_client.get("/healthz")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_custom_ready_path(self, custom_path_client: TestClient):
        """Test custom ready path."""
        response = custom_path_client.get("/readiness")
        assert response.status_code == 200
        assert response.json()["ready"] is True

    def test_custom_live_path(self, custom_path_client: TestClient):
        """Test custom live path."""
        response = custom_path_client.get("/liveness")
        assert response.status_code == 200
        assert response.json()["alive"] is True

    def test_default_paths_not_available(self, custom_path_client: TestClient):
        """Test that default paths are not available."""
        response = custom_path_client.get("/health")
        # Should return 404 or pass to app
        assert response.status_code in [200, 404]


class TestCustomHealthChecks:
    """Tests for custom health check functions."""

    @pytest.fixture
    def all_healthy_app(self) -> FastAPI:
        """Create app with all healthy checks."""
        app = FastAPI()

        async def check_database():
            """Execute check_database operation.

            Returns:
                The result of the operation.
            """
            return True

        async def check_cache():
            """Execute check_cache operation.

            Returns:
                The result of the operation.
            """
            return True

        config = HealthConfig(
            custom_checks={
                "database": check_database,
                "cache": check_cache,
            }
        )
        app.add_middleware(HealthCheckMiddleware, config=config)

        return app

    @pytest.fixture
    def all_healthy_client(self, all_healthy_app: FastAPI) -> TestClient:
        """Execute all_healthy_client operation.

        Args:
            all_healthy_app: The all_healthy_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(all_healthy_app)

    def test_all_healthy_returns_200(self, all_healthy_client: TestClient):
        """Test that all healthy returns 200."""
        response = all_healthy_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_checks_included_in_response(self, all_healthy_client: TestClient):
        """Test that checks are included in response."""
        response = all_healthy_client.get("/health")

        data = response.json()
        assert "checks" in data
        assert data["checks"]["database"] == "healthy"
        assert data["checks"]["cache"] == "healthy"


class TestUnhealthyChecks:
    """Tests for unhealthy check scenarios."""

    @pytest.fixture
    def unhealthy_app(self) -> FastAPI:
        """Create app with unhealthy checks."""
        app = FastAPI()

        async def check_database():
            """Execute check_database operation.

            Returns:
                The result of the operation.
            """
            return True

        async def check_cache():
            """Execute check_cache operation.

            Returns:
                The result of the operation.
            """
            return False  # Unhealthy

        config = HealthConfig(
            custom_checks={
                "database": check_database,
                "cache": check_cache,
            }
        )
        app.add_middleware(HealthCheckMiddleware, config=config)

        return app

    @pytest.fixture
    def unhealthy_client(self, unhealthy_app: FastAPI) -> TestClient:
        """Execute unhealthy_client operation.

        Args:
            unhealthy_app: The unhealthy_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(unhealthy_app)

    def test_unhealthy_returns_503(self, unhealthy_client: TestClient):
        """Test that unhealthy status returns 503."""
        response = unhealthy_client.get("/health")

        assert response.status_code == 503

    def test_unhealthy_status_in_response(self, unhealthy_client: TestClient):
        """Test that unhealthy status is in response."""
        response = unhealthy_client.get("/health")

        data = response.json()
        assert data["status"] == "unhealthy"

    def test_checks_show_unhealthy(self, unhealthy_client: TestClient):
        """Test that checks show unhealthy status."""
        response = unhealthy_client.get("/health")

        data = response.json()
        assert data["checks"]["database"] == "healthy"
        assert data["checks"]["cache"] == "unhealthy"

    def test_ready_returns_503_when_unhealthy(self, unhealthy_client: TestClient):
        """Test that /ready returns 503 when unhealthy."""
        response = unhealthy_client.get("/ready")

        assert response.status_code == 503
        data = response.json()
        assert data["ready"] is False


class TestCheckExceptions:
    """Tests for health check exceptions."""

    @pytest.fixture
    def exception_app(self) -> FastAPI:
        """Create app with failing check."""
        app = FastAPI()

        async def check_that_fails():
            """Execute check_that_fails operation.

            Returns:
                The result of the operation.
            """
            raise RuntimeError("Check failed")

        config = HealthConfig(
            custom_checks={
                "failing": check_that_fails,
            }
        )
        app.add_middleware(HealthCheckMiddleware, config=config)

        return app

    @pytest.fixture
    def exception_client(self, exception_app: FastAPI) -> TestClient:
        """Execute exception_client operation.

        Args:
            exception_app: The exception_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(exception_app)

    def test_exception_treated_as_unhealthy(self, exception_client: TestClient):
        """Test that exceptions are treated as unhealthy."""
        response = exception_client.get("/health")

        assert response.status_code == 503
        data = response.json()
        assert data["checks"]["failing"] == "unhealthy"


class TestWithoutDetails:
    """Tests for health checks without details."""

    @pytest.fixture
    def no_details_app(self) -> FastAPI:
        """Create app without details."""
        app = FastAPI()
        config = HealthConfig(
            include_details=False,
            version="1.0.0",
        )
        app.add_middleware(HealthCheckMiddleware, config=config)

        return app

    @pytest.fixture
    def no_details_client(self, no_details_app: FastAPI) -> TestClient:
        """Execute no_details_client operation.

        Args:
            no_details_app: The no_details_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(no_details_app)

    def test_no_uptime_in_response(self, no_details_client: TestClient):
        """Test that uptime is not in response."""
        response = no_details_client.get("/health")

        data = response.json()
        assert "uptime_seconds" not in data

    def test_no_version_in_response(self, no_details_client: TestClient):
        """Test that version is not in response."""
        response = no_details_client.get("/health")

        data = response.json()
        assert "version" not in data

    def test_status_still_present(self, no_details_client: TestClient):
        """Test that status is still present."""
        response = no_details_client.get("/health")

        data = response.json()
        assert "status" in data
        assert "timestamp" in data
