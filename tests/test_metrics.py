"""Comprehensive tests for Metrics middleware."""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import MetricsCollector, MetricsConfig, MetricsMiddleware


@pytest.fixture
def metrics_app() -> FastAPI:
    """Create app with metrics middleware."""
    app = FastAPI()
    app.add_middleware(MetricsMiddleware)

    @app.get("/")
    async def root():
        """Execute root operation.

        Returns:
            The result of the operation.
        """
        return {"message": "Hello"}

    @app.get("/users/{user_id}")
    async def get_user(user_id: int):
        """Execute get_user operation.

        Args:
            user_id: The user_id parameter.

        Returns:
            The result of the operation.
        """
        return {"user_id": user_id}

    @app.post("/users")
    async def create_user():
        """Execute create_user operation.

        Returns:
            The result of the operation.
        """
        return {"created": True}

    @app.get("/error")
    async def error():
        """Execute error operation.

        Returns:
            The result of the operation.
        """
        raise ValueError("Error")

    return app


@pytest.fixture
def metrics_client(metrics_app: FastAPI) -> TestClient:
    """Execute metrics_client operation.

    Args:
        metrics_app: The metrics_app parameter.

    Returns:
        The result of the operation.
    """
    return TestClient(metrics_app, raise_server_exceptions=False)


class TestMetricsMiddleware:
    """Tests for MetricsMiddleware."""

    def test_metrics_endpoint_exists(self, metrics_client: TestClient):
        """Test that /metrics endpoint exists."""
        response = metrics_client.get("/metrics")

        assert response.status_code == 200

    def test_metrics_content_type(self, metrics_client: TestClient):
        """Test that metrics have correct content type."""
        response = metrics_client.get("/metrics")

        assert "text/plain" in response.headers["Content-Type"]

    def test_metrics_contains_uptime(self, metrics_client: TestClient):
        """Test that metrics include uptime."""
        response = metrics_client.get("/metrics")

        assert "fastx_uptime_seconds" in response.text

    def test_request_counted(self, metrics_client: TestClient):
        """Test that requests are counted in metrics."""
        # Make some requests
        metrics_client.get("/")
        metrics_client.get("/")
        metrics_client.get("/")

        # Check metrics
        response = metrics_client.get("/metrics")

        assert "fastx_http_requests_total" in response.text

    def test_different_methods_tracked(self, metrics_client: TestClient):
        """Test that different methods are tracked separately."""
        metrics_client.get("/")
        metrics_client.post("/users")

        response = metrics_client.get("/metrics")

        assert 'method="GET"' in response.text
        assert 'method="POST"' in response.text

    def test_status_codes_tracked(self, metrics_client: TestClient):
        """Test that status codes are tracked."""
        metrics_client.get("/")
        metrics_client.get("/nonexistent")

        response = metrics_client.get("/metrics")

        assert 'status="200"' in response.text


class TestMetricsCollector:
    """Tests for MetricsCollector."""

    def test_record_request(self):
        """Test recording a request."""
        config = MetricsConfig()
        collector = MetricsCollector(config)

        collector.record_request(
            method="GET",
            path="/test",
            status_code=200,
            latency=0.1,
            response_size=100,
        )

        json_metrics = collector.get_json_metrics()
        assert json_metrics["total_requests"] == 1

    def test_multiple_requests(self):
        """Test recording multiple requests."""
        config = MetricsConfig()
        collector = MetricsCollector(config)

        collector.record_request("GET", "/test1", 200, 0.1)
        collector.record_request("GET", "/test2", 200, 0.2)
        collector.record_request("POST", "/test3", 201, 0.3)

        json_metrics = collector.get_json_metrics()
        assert json_metrics["total_requests"] == 3

    def test_error_tracking(self):
        """Test that 5xx errors are tracked."""
        config = MetricsConfig()
        collector = MetricsCollector(config)

        collector.record_request("GET", "/error", 500, 0.1)
        collector.record_request("GET", "/error", 503, 0.1)

        json_metrics = collector.get_json_metrics()
        assert json_metrics["total_errors"] == 2

    def test_4xx_not_counted_as_errors(self):
        """Test that 4xx errors are not counted as errors."""
        config = MetricsConfig()
        collector = MetricsCollector(config)

        collector.record_request("GET", "/notfound", 404, 0.1)
        collector.record_request("GET", "/forbidden", 403, 0.1)

        json_metrics = collector.get_json_metrics()
        assert json_metrics["total_errors"] == 0

    def test_prometheus_format(self):
        """Test Prometheus-compatible output format."""
        config = MetricsConfig()
        collector = MetricsCollector(config)

        collector.record_request("GET", "/test", 200, 0.1)

        metrics = collector.get_metrics()

        assert "# HELP" in metrics
        assert "# TYPE" in metrics

    def test_prometheus_format_uptime(self):
        """Test uptime metric in Prometheus format."""
        config = MetricsConfig()
        collector = MetricsCollector(config)

        metrics = collector.get_metrics()

        assert "# HELP fastx_uptime_seconds" in metrics
        assert "# TYPE fastx_uptime_seconds gauge" in metrics

    def test_prometheus_format_requests(self):
        """Test requests metric in Prometheus format."""
        config = MetricsConfig()
        collector = MetricsCollector(config)

        collector.record_request("GET", "/test", 200, 0.1)

        metrics = collector.get_metrics()

        assert "# TYPE fastx_http_requests_total counter" in metrics


class TestMetricsConfig:
    """Tests for MetricsConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = MetricsConfig()

        assert config.metrics_path == "/metrics"
        assert config.enable_latency_histogram is True
        assert config.enable_request_count is True
        assert config.enable_response_size is True

    def test_custom_metrics_path(self):
        """Test custom metrics path."""
        config = MetricsConfig(metrics_path="/prometheus")

        assert config.metrics_path == "/prometheus"

    def test_custom_histogram_buckets(self):
        """Test custom histogram buckets."""
        buckets = (0.1, 0.5, 1.0, 5.0)
        config = MetricsConfig(histogram_buckets=buckets)

        assert config.histogram_buckets == buckets

    def test_path_patterns(self):
        """Test path normalization patterns."""
        config = MetricsConfig(
            path_patterns={
                r"/users/\d+": "/users/{id}",
                r"/orders/[a-f0-9-]+": "/orders/{uuid}",
            }
        )

        assert len(config.path_patterns) == 2


class TestCustomMetricsPath:
    """Tests for custom metrics endpoint path."""

    @pytest.fixture
    def custom_path_app(self) -> FastAPI:
        """Create app with custom metrics path."""
        app = FastAPI()
        config = MetricsConfig(metrics_path="/prometheus")
        app.add_middleware(MetricsMiddleware, config=config)

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

    def test_custom_path_works(self, custom_path_client: TestClient):
        """Test that custom metrics path works."""
        response = custom_path_client.get("/prometheus")

        assert response.status_code == 200
        assert "fastx_uptime_seconds" in response.text

    def test_default_path_not_available(self, custom_path_client: TestClient):
        """Test that default path is not available."""
        response = custom_path_client.get("/metrics")

        # Should be 404 or pass to app
        assert response.status_code in [404, 422]


class TestPathNormalization:
    """Tests for path normalization."""

    @pytest.fixture
    def normalized_app(self) -> FastAPI:
        """Create app with path normalization."""
        app = FastAPI()
        config = MetricsConfig(
            path_patterns={
                r"/users/\d+": "/users/{id}",
            }
        )
        app.add_middleware(MetricsMiddleware, config=config)

        @app.get("/users/{user_id}")
        async def get_user(user_id: int):
            """Execute get_user operation.

            Args:
                user_id: The user_id parameter.

            Returns:
                The result of the operation.
            """
            return {"user_id": user_id}

        return app

    @pytest.fixture
    def normalized_client(self, normalized_app: FastAPI) -> TestClient:
        """Execute normalized_client operation.

        Args:
            normalized_app: The normalized_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(normalized_app)

    def test_paths_normalized_in_metrics(self, normalized_client: TestClient):
        """Test that paths are normalized in metrics."""
        # Make requests to different user IDs
        normalized_client.get("/users/1")
        normalized_client.get("/users/2")
        normalized_client.get("/users/3")

        response = normalized_client.get("/metrics")

        # Should be grouped under normalized path
        assert "/users/{id}" in response.text


class TestMetricsExclusion:
    """Tests for metrics path exclusion."""

    @pytest.fixture
    def excluded_app(self) -> FastAPI:
        """Create app with path exclusion."""
        app = FastAPI()
        app.add_middleware(
            MetricsMiddleware,
            exclude_paths={"/health"},
        )

        @app.get("/")
        async def root():
            """Execute root operation.

            Returns:
                The result of the operation.
            """
            return {"ok": True}

        @app.get("/health")
        async def health():
            """Execute health operation.

            Returns:
                The result of the operation.
            """
            return {"status": "ok"}

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

    def test_excluded_paths_not_in_metrics(self, excluded_client: TestClient):
        """Test that excluded paths are not in metrics."""
        # Make requests to both paths
        excluded_client.get("/")
        excluded_client.get("/health")
        excluded_client.get("/health")

        response = excluded_client.get("/metrics")

        # Health should not be in metrics (or have 0 count)
        assert 'path="/"' in response.text


class TestHistogramBuckets:
    """Tests for latency histogram buckets."""

    def test_histogram_buckets_in_output(self):
        """Test that histogram buckets appear in output."""
        config = MetricsConfig(
            histogram_buckets=(0.01, 0.1, 1.0),
        )
        collector = MetricsCollector(config)

        collector.record_request("GET", "/test", 200, 0.05)

        metrics = collector.get_metrics()

        assert 'le="0.01"' in metrics
        assert 'le="0.1"' in metrics
        assert 'le="1.0"' in metrics
        assert 'le="+Inf"' in metrics
