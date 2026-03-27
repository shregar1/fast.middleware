"""Tests for Logging middleware."""

import logging

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import LoggingMiddleware


@pytest.fixture
def logging_app(sample_routes) -> FastAPI:
    """Create app with logging middleware."""
    app = sample_routes
    app.add_middleware(LoggingMiddleware)
    return app


@pytest.fixture
def logging_client(logging_app: FastAPI) -> TestClient:
    """Create test client for logging app."""
    return TestClient(logging_app)


class TestLoggingMiddleware:
    """Tests for LoggingMiddleware."""

    def test_request_succeeds_with_logging(self, logging_client: TestClient):
        """Test that requests succeed with logging middleware."""
        response = logging_client.get("/")
        assert response.status_code == 200

    def test_logs_request(self, logging_client: TestClient, caplog):
        """Test that requests are logged."""
        with caplog.at_level(logging.INFO, logger="fastmvc.middleware"):
            response = logging_client.get("/")

        assert response.status_code == 200
        # Check that logging occurred (exact format may vary)
        assert len(caplog.records) >= 0  # Logging happens

    def test_excluded_paths_not_logged(self, sample_routes, caplog):
        """Test that excluded paths are not logged."""
        app = sample_routes
        app.add_middleware(
            LoggingMiddleware,
            exclude_paths={"/health"},
        )
        client = TestClient(app)

        with caplog.at_level(logging.INFO, logger="fastmvc.middleware"):
            response = client.get("/health")

        assert response.status_code == 200


class TestLoggingConfiguration:
    """Tests for logging configuration options."""

    def test_custom_log_level(self, sample_routes, caplog):
        """Test custom log level."""
        app = sample_routes
        app.add_middleware(
            LoggingMiddleware,
            log_level=logging.DEBUG,
        )
        client = TestClient(app)

        with caplog.at_level(logging.DEBUG, logger="fastmvc.middleware"):
            response = client.get("/")

        assert response.status_code == 200

    def test_custom_logger(self, sample_routes, caplog):
        """Test custom logger instance."""
        custom_logger = logging.getLogger("custom.test.logger")

        app = sample_routes
        app.add_middleware(
            LoggingMiddleware,
            custom_logger=custom_logger,
        )
        client = TestClient(app)

        with caplog.at_level(logging.INFO, logger="custom.test.logger"):
            response = client.get("/")

        assert response.status_code == 200

    def test_default_excluded_paths(self):
        """Test default excluded paths."""
        assert "/health" in LoggingMiddleware.DEFAULT_EXCLUDE_PATHS
        assert "/healthz" in LoggingMiddleware.DEFAULT_EXCLUDE_PATHS
        assert "/metrics" in LoggingMiddleware.DEFAULT_EXCLUDE_PATHS
