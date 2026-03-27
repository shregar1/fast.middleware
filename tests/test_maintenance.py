"""Comprehensive tests for Maintenance Mode middleware."""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import MaintenanceConfig, MaintenanceMiddleware


class TestMaintenanceModeDisabled:
    """Tests for maintenance mode when disabled."""

    @pytest.fixture
    def disabled_app(self) -> FastAPI:
        """Create app with maintenance mode disabled."""
        app = FastAPI()
        app.add_middleware(MaintenanceMiddleware, enabled=False)

        @app.get("/")
        async def root():
            """Execute root operation.

            Returns:
                The result of the operation.
            """
            return {"message": "Hello"}

        @app.post("/data")
        async def create_data():
            """Execute create_data operation.

            Returns:
                The result of the operation.
            """
            return {"created": True}

        return app

    @pytest.fixture
    def disabled_client(self, disabled_app: FastAPI) -> TestClient:
        """Execute disabled_client operation.

        Args:
            disabled_app: The disabled_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(disabled_app)

    def test_get_passes_through(self, disabled_client: TestClient):
        """Test that GET requests pass through when disabled."""
        response = disabled_client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello"}

    def test_post_passes_through(self, disabled_client: TestClient):
        """Test that POST requests pass through when disabled."""
        response = disabled_client.post("/data")

        assert response.status_code == 200
        assert response.json() == {"created": True}

    def test_no_maintenance_header(self, disabled_client: TestClient):
        """Test that no maintenance header is present."""
        response = disabled_client.get("/")

        assert "X-Maintenance-Mode" not in response.headers


class TestMaintenanceModeEnabled:
    """Tests for maintenance mode when enabled."""

    @pytest.fixture
    def enabled_app(self) -> FastAPI:
        """Create app with maintenance mode enabled."""
        app = FastAPI()
        config = MaintenanceConfig(
            enabled=True,
            message="Under maintenance",
            retry_after=300,
        )
        app.add_middleware(MaintenanceMiddleware, config=config)

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

    @pytest.fixture
    def enabled_client(self, enabled_app: FastAPI) -> TestClient:
        """Execute enabled_client operation.

        Args:
            enabled_app: The enabled_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(enabled_app)

    def test_returns_503(self, enabled_client: TestClient):
        """Test that 503 is returned during maintenance."""
        response = enabled_client.get("/")

        assert response.status_code == 503

    def test_returns_maintenance_message(self, enabled_client: TestClient):
        """Test that maintenance message is returned."""
        response = enabled_client.get("/")

        data = response.json()
        assert data["message"] == "Under maintenance"

    def test_maintenance_flag_in_response(self, enabled_client: TestClient):
        """Test that maintenance flag is in response."""
        response = enabled_client.get("/")

        data = response.json()
        assert data["maintenance"] is True

    def test_retry_after_in_response(self, enabled_client: TestClient):
        """Test that retry_after is in response."""
        response = enabled_client.get("/")

        data = response.json()
        assert data["retry_after"] == 300

    def test_retry_after_header(self, enabled_client: TestClient):
        """Test that Retry-After header is set."""
        response = enabled_client.get("/")

        assert response.headers.get("Retry-After") == "300"

    def test_maintenance_mode_header(self, enabled_client: TestClient):
        """Test that X-Maintenance-Mode header is set."""
        response = enabled_client.get("/")

        assert response.headers.get("X-Maintenance-Mode") == "true"

    def test_error_flag_in_response(self, enabled_client: TestClient):
        """Test that error flag is in response."""
        response = enabled_client.get("/")

        data = response.json()
        assert data["error"] is True


class TestMaintenanceBypass:
    """Tests for maintenance mode bypass."""

    @pytest.fixture
    def bypass_app(self) -> FastAPI:
        """Create app with bypass options."""
        app = FastAPI()
        config = MaintenanceConfig(
            enabled=True,
            allowed_paths={"/health", "/status"},
            allowed_ips={"127.0.0.1", "10.0.0.1"},
            bypass_token="secret-token",
        )
        app.add_middleware(MaintenanceMiddleware, config=config)

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

        @app.get("/status")
        async def status():
            """Execute status operation.

            Returns:
                The result of the operation.
            """
            return {"status": "running"}

        return app

    @pytest.fixture
    def bypass_client(self, bypass_app: FastAPI) -> TestClient:
        """Execute bypass_client operation.

        Args:
            bypass_app: The bypass_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(bypass_app)

    def test_allowed_path_bypasses(self, bypass_client: TestClient):
        """Test that allowed paths bypass maintenance."""
        response = bypass_client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_multiple_allowed_paths(self, bypass_client: TestClient):
        """Test that multiple allowed paths work."""
        response = bypass_client.get("/status")

        assert response.status_code == 200

    def test_bypass_token_works(self, bypass_client: TestClient):
        """Test that bypass token allows access."""
        response = bypass_client.get(
            "/", headers={"X-Maintenance-Bypass": "secret-token"}
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Hello"}

    def test_wrong_bypass_token_blocked(self, bypass_client: TestClient):
        """Test that wrong bypass token is blocked."""
        response = bypass_client.get(
            "/", headers={"X-Maintenance-Bypass": "wrong-token"}
        )

        assert response.status_code == 503

    def test_non_allowed_path_blocked(self, bypass_client: TestClient):
        """Test that non-allowed paths are blocked."""
        response = bypass_client.get("/")

        assert response.status_code == 503


class TestMaintenanceConfig:
    """Tests for MaintenanceConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = MaintenanceConfig()

        assert config.enabled is False
        assert config.retry_after == 300
        assert config.bypass_header == "X-Maintenance-Bypass"
        assert config.use_html is False

    def test_custom_config(self):
        """Test custom configuration values."""
        config = MaintenanceConfig(
            enabled=True,
            message="Custom message",
            retry_after=600,
            use_html=True,
        )

        assert config.enabled is True
        assert config.message == "Custom message"
        assert config.retry_after == 600
        assert config.use_html is True

    def test_allowed_paths_config(self):
        """Test allowed paths configuration."""
        config = MaintenanceConfig(
            allowed_paths={"/health", "/metrics"},
        )

        assert "/health" in config.allowed_paths
        assert "/metrics" in config.allowed_paths

    def test_allowed_ips_config(self):
        """Test allowed IPs configuration."""
        config = MaintenanceConfig(
            allowed_ips={"10.0.0.1", "192.168.1.1"},
        )

        assert "10.0.0.1" in config.allowed_ips
        assert "192.168.1.1" in config.allowed_ips


class TestDynamicToggle:
    """Tests for dynamically enabling/disabling maintenance."""

    def test_enable_method(self):
        """Test enable method."""
        app = FastAPI()
        config = MaintenanceConfig(enabled=False)
        middleware = MaintenanceMiddleware(app, config=config)

        assert middleware.is_enabled() is False

        middleware.enable()
        assert middleware.is_enabled() is True

    def test_disable_method(self):
        """Test disable method."""
        app = FastAPI()
        config = MaintenanceConfig(enabled=True)
        middleware = MaintenanceMiddleware(app, config=config)

        assert middleware.is_enabled() is True

        middleware.disable()
        assert middleware.is_enabled() is False

    def test_enable_with_message(self):
        """Test enable with custom message."""
        app = FastAPI()
        config = MaintenanceConfig(enabled=False)
        middleware = MaintenanceMiddleware(app, config=config)

        middleware.enable(message="Deploying new version")

        assert middleware.config.message == "Deploying new version"

    def test_enable_with_retry_after(self):
        """Test enable with custom retry after."""
        app = FastAPI()
        config = MaintenanceConfig(enabled=False, retry_after=300)
        middleware = MaintenanceMiddleware(app, config=config)

        middleware.enable(retry_after=600)

        assert middleware.config.retry_after == 600


class TestHtmlMode:
    """Tests for HTML maintenance page."""

    @pytest.fixture
    def html_app(self) -> FastAPI:
        """Create app with HTML maintenance mode."""
        app = FastAPI()
        config = MaintenanceConfig(
            enabled=True,
            use_html=True,
            message="We're upgrading!",
            retry_after=1800,
        )
        app.add_middleware(MaintenanceMiddleware, config=config)

        @app.get("/")
        async def root():
            """Execute root operation.

            Returns:
                The result of the operation.
            """
            return {"ok": True}

        return app

    @pytest.fixture
    def html_client(self, html_app: FastAPI) -> TestClient:
        """Execute html_client operation.

        Args:
            html_app: The html_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(html_app)

    def test_returns_html(self, html_client: TestClient):
        """Test that HTML is returned."""
        response = html_client.get("/")

        assert response.status_code == 503
        assert "text/html" in response.headers["Content-Type"]

    def test_html_contains_message(self, html_client: TestClient):
        """Test that HTML contains message."""
        response = html_client.get("/")

        assert "We're upgrading!" in response.text

    def test_html_contains_retry_time(self, html_client: TestClient):
        """Test that HTML contains retry time."""
        response = html_client.get("/")

        # 1800 seconds = 30 minutes
        assert "30" in response.text


class TestCustomHtmlTemplate:
    """Tests for custom HTML template."""

    @pytest.fixture
    def custom_html_app(self) -> FastAPI:
        """Create app with custom HTML template."""
        app = FastAPI()
        config = MaintenanceConfig(
            enabled=True,
            use_html=True,
            html_template="<h1>Custom: {message}</h1><p>Retry in {retry_minutes} min</p>",
            message="System update",
            retry_after=600,
        )
        app.add_middleware(MaintenanceMiddleware, config=config)

        @app.get("/")
        async def root():
            """Execute root operation.

            Returns:
                The result of the operation.
            """
            return {"ok": True}

        return app

    @pytest.fixture
    def custom_html_client(self, custom_html_app: FastAPI) -> TestClient:
        """Execute custom_html_client operation.

        Args:
            custom_html_app: The custom_html_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(custom_html_app)

    def test_custom_template_used(self, custom_html_client: TestClient):
        """Test that custom template is used."""
        response = custom_html_client.get("/")

        assert "Custom: System update" in response.text
        assert "10 min" in response.text


class TestPathExclusion:
    """Tests for path exclusion via middleware."""

    @pytest.fixture
    def excluded_app(self) -> FastAPI:
        """Create app with path exclusion."""
        app = FastAPI()
        config = MaintenanceConfig(enabled=True)
        app.add_middleware(
            MaintenanceMiddleware,
            config=config,
            exclude_paths={"/excluded"},
        )

        @app.get("/included")
        async def included():
            """Execute included operation.

            Returns:
                The result of the operation.
            """
            return {"ok": True}

        @app.get("/excluded")
        async def excluded():
            """Execute excluded operation.

            Returns:
                The result of the operation.
            """
            return {"ok": True}

        return app

    @pytest.fixture
    def excluded_client(self, excluded_app: FastAPI) -> TestClient:
        """Execute excluded_client operation.

        Args:
            excluded_app: The excluded_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(excluded_app)

    def test_excluded_path_bypasses(self, excluded_client: TestClient):
        """Test that excluded paths bypass maintenance."""
        response = excluded_client.get("/excluded")

        assert response.status_code == 200

    def test_included_path_blocked(self, excluded_client: TestClient):
        """Test that included paths are blocked."""
        response = excluded_client.get("/included")

        assert response.status_code == 503


class TestMethodExclusion:
    """Tests for HTTP method exclusion."""

    @pytest.fixture
    def method_excluded_app(self) -> FastAPI:
        """Create app with method exclusion."""
        app = FastAPI()
        config = MaintenanceConfig(enabled=True)
        app.add_middleware(
            MaintenanceMiddleware,
            config=config,
            exclude_methods={"OPTIONS", "HEAD"},
        )

        @app.get("/")
        async def root():
            """Execute root operation.

            Returns:
                The result of the operation.
            """
            return {"ok": True}

        @app.options("/")
        async def options():
            """Execute options operation.

            Returns:
                The result of the operation.
            """
            return {}

        return app

    @pytest.fixture
    def method_excluded_client(self, method_excluded_app: FastAPI) -> TestClient:
        """Execute method_excluded_client operation.

        Args:
            method_excluded_app: The method_excluded_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(method_excluded_app)

    def test_excluded_method_bypasses(self, method_excluded_client: TestClient):
        """Test that excluded methods bypass maintenance."""
        response = method_excluded_client.options("/")

        # OPTIONS should bypass
        assert response.status_code in [200, 204]

    def test_included_method_blocked(self, method_excluded_client: TestClient):
        """Test that included methods are blocked."""
        response = method_excluded_client.get("/")

        assert response.status_code == 503
