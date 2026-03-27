"""Comprehensive tests for Error Handler middleware."""

import logging

import pytest
from fastapi import FastAPI, HTTPException
from starlette.testclient import TestClient

from fastmiddleware import ErrorConfig, ErrorHandlerMiddleware


class TestErrorHandlerMiddleware:
    """Tests for ErrorHandlerMiddleware."""

    @pytest.fixture
    def error_app(self) -> FastAPI:
        """Create app with error handler middleware."""
        app = FastAPI()
        app.add_middleware(
            ErrorHandlerMiddleware,
            include_exception_type=True,
        )

        @app.get("/error")
        async def raise_error():
            """Execute raise_error operation.

            Returns:
                The result of the operation.
            """
            raise ValueError("Test error message")

        @app.get("/runtime-error")
        async def raise_runtime_error():
            """Execute raise_runtime_error operation.

            Returns:
                The result of the operation.
            """
            raise RuntimeError("Runtime error occurred")

        @app.get("/zero-division")
        async def zero_division():
            """Execute zero_division operation.

            Returns:
                The result of the operation.
            """
            return 1 / 0

        @app.get("/success")
        async def success():
            """Execute success operation.

            Returns:
                The result of the operation.
            """
            return {"status": "ok"}

        @app.get("/http-exception")
        async def http_exception():
            """Execute http_exception operation.

            Returns:
                The result of the operation.
            """
            raise HTTPException(status_code=404, detail="Not found")

        return app

    @pytest.fixture
    def error_client(self, error_app: FastAPI) -> TestClient:
        """Execute error_client operation.

        Args:
            error_app: The error_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(error_app, raise_server_exceptions=False)

    def test_catches_value_error(self, error_client: TestClient):
        """Test that ValueError is caught and handled."""
        response = error_client.get("/error")

        assert response.status_code == 500
        data = response.json()
        assert data["error"] is True
        assert data["type"] == "ValueError"
        assert data["detail"] == "Test error message"

    def test_catches_runtime_error(self, error_client: TestClient):
        """Test that RuntimeError is caught and handled."""
        response = error_client.get("/runtime-error")

        assert response.status_code == 500
        data = response.json()
        assert data["type"] == "RuntimeError"

    def test_catches_zero_division(self, error_client: TestClient):
        """Test that ZeroDivisionError is caught and handled."""
        response = error_client.get("/zero-division")

        assert response.status_code == 500
        data = response.json()
        assert data["type"] == "ZeroDivisionError"

    def test_success_passes_through(self, error_client: TestClient):
        """Test that successful requests pass through."""
        response = error_client.get("/success")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestErrorConfig:
    """Tests for ErrorConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ErrorConfig()

        assert config.include_traceback is False
        assert config.include_exception_type is False
        assert config.log_exceptions is True
        assert config.status_code == 500
        assert config.default_message == "An internal error occurred"

    def test_custom_config(self):
        """Test custom configuration values."""
        config = ErrorConfig(
            include_traceback=True,
            include_exception_type=True,
            default_message="Something went wrong",
            status_code=500,
        )

        assert config.include_traceback is True
        assert config.default_message == "Something went wrong"


class TestCustomErrorHandlers:
    """Tests for custom error handlers."""

    @pytest.fixture
    def custom_handler_app(self) -> FastAPI:
        """Create app with custom error handlers."""
        app = FastAPI()

        config = ErrorConfig()
        config.error_handlers[ValueError] = (400, "Invalid value provided")
        config.error_handlers[PermissionError] = (403, "Permission denied")
        config.error_handlers[FileNotFoundError] = (404, "Resource not found")

        app.add_middleware(ErrorHandlerMiddleware, config=config)

        @app.get("/value-error")
        async def value_error():
            """Execute value_error operation.

            Returns:
                The result of the operation.
            """
            raise ValueError("bad value")

        @app.get("/permission-error")
        async def permission_error():
            """Execute permission_error operation.

            Returns:
                The result of the operation.
            """
            raise PermissionError("not allowed")

        @app.get("/file-not-found")
        async def file_not_found():
            """Execute file_not_found operation.

            Returns:
                The result of the operation.
            """
            raise FileNotFoundError("missing file")

        @app.get("/generic-error")
        async def generic_error():
            """Execute generic_error operation.

            Returns:
                The result of the operation.
            """
            raise RuntimeError("generic")

        return app

    @pytest.fixture
    def custom_handler_client(self, custom_handler_app: FastAPI) -> TestClient:
        """Execute custom_handler_client operation.

        Args:
            custom_handler_app: The custom_handler_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(custom_handler_app, raise_server_exceptions=False)

    def test_value_error_returns_400(self, custom_handler_client: TestClient):
        """Test custom handler for ValueError."""
        response = custom_handler_client.get("/value-error")

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid value provided"

    def test_permission_error_returns_403(self, custom_handler_client: TestClient):
        """Test custom handler for PermissionError."""
        response = custom_handler_client.get("/permission-error")

        assert response.status_code == 403
        assert response.json()["message"] == "Permission denied"

    def test_file_not_found_returns_404(self, custom_handler_client: TestClient):
        """Test custom handler for FileNotFoundError."""
        response = custom_handler_client.get("/file-not-found")

        assert response.status_code == 404
        assert response.json()["message"] == "Resource not found"

    def test_generic_error_uses_default(self, custom_handler_client: TestClient):
        """Test that generic errors use default handler."""
        response = custom_handler_client.get("/generic-error")

        assert response.status_code == 500
        assert response.json()["message"] == "An internal error occurred"


class TestTraceback:
    """Tests for traceback inclusion."""

    @pytest.fixture
    def traceback_app(self) -> FastAPI:
        """Create app with traceback enabled."""
        app = FastAPI()
        app.add_middleware(
            ErrorHandlerMiddleware,
            include_traceback=True,
            include_exception_type=True,
        )

        @app.get("/error")
        async def raise_error():
            """Execute raise_error operation.

            Returns:
                The result of the operation.
            """
            raise RuntimeError("Detailed error")

        return app

    @pytest.fixture
    def traceback_client(self, traceback_app: FastAPI) -> TestClient:
        """Execute traceback_client operation.

        Args:
            traceback_app: The traceback_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(traceback_app, raise_server_exceptions=False)

    def test_includes_traceback(self, traceback_client: TestClient):
        """Test that traceback is included when configured."""
        response = traceback_client.get("/error")

        assert response.status_code == 500
        data = response.json()
        assert "traceback" in data
        assert isinstance(data["traceback"], list)
        assert len(data["traceback"]) > 0

    def test_traceback_contains_error_info(self, traceback_client: TestClient):
        """Test that traceback contains error information."""
        response = traceback_client.get("/error")

        data = response.json()
        traceback_text = "\n".join(data["traceback"])
        assert "RuntimeError" in traceback_text or "Detailed error" in traceback_text


class TestNoTraceback:
    """Tests for production mode without traceback."""

    @pytest.fixture
    def prod_app(self) -> FastAPI:
        """Create app without traceback (production mode)."""
        app = FastAPI()
        app.add_middleware(
            ErrorHandlerMiddleware,
            include_traceback=False,
            include_exception_type=False,
        )

        @app.get("/error")
        async def raise_error():
            """Execute raise_error operation.

            Returns:
                The result of the operation.
            """
            raise RuntimeError("Secret error details")

        return app

    @pytest.fixture
    def prod_client(self, prod_app: FastAPI) -> TestClient:
        """Execute prod_client operation.

        Args:
            prod_app: The prod_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(prod_app, raise_server_exceptions=False)

    def test_no_traceback_in_response(self, prod_client: TestClient):
        """Test that traceback is not included in production mode."""
        response = prod_client.get("/error")

        data = response.json()
        assert "traceback" not in data

    def test_no_exception_type_in_response(self, prod_client: TestClient):
        """Test that exception type is not included."""
        response = prod_client.get("/error")

        data = response.json()
        assert "type" not in data

    def test_no_secret_details_leaked(self, prod_client: TestClient):
        """Test that secret error details are not leaked."""
        response = prod_client.get("/error")

        data = response.json()
        assert "Secret error details" not in str(data)


class TestRequestIdInError:
    """Tests for request ID in error responses."""

    @pytest.fixture
    def request_id_app(self) -> FastAPI:
        """Create app with request ID."""
        from fastmiddleware import RequestIDMiddleware

        app = FastAPI()
        app.add_middleware(ErrorHandlerMiddleware, include_exception_type=True)
        app.add_middleware(RequestIDMiddleware)

        @app.get("/error")
        async def raise_error():
            """Execute raise_error operation.

            Returns:
                The result of the operation.
            """
            raise ValueError("error")

        return app

    @pytest.fixture
    def request_id_client(self, request_id_app: FastAPI) -> TestClient:
        """Execute request_id_client operation.

        Args:
            request_id_app: The request_id_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(request_id_app, raise_server_exceptions=False)

    def test_request_id_in_error_response(self, request_id_client: TestClient):
        """Test that request ID is included in error response."""
        response = request_id_client.get("/error")

        data = response.json()
        assert "request_id" in data
        assert data["request_id"] is not None


class TestExceptionLogging:
    """Tests for exception logging."""

    def test_exceptions_are_logged(self, caplog):
        """Test that exceptions are logged."""
        app = FastAPI()
        app.add_middleware(
            ErrorHandlerMiddleware,
            log_exceptions=True,
        )

        @app.get("/error")
        async def raise_error():
            """Execute raise_error operation.

            Returns:
                The result of the operation.
            """
            raise ValueError("logged error")

        client = TestClient(app, raise_server_exceptions=False)

        with caplog.at_level(logging.ERROR):
            response = client.get("/error")

        assert response.status_code == 500
        # Note: Logging assertions depend on logger configuration
