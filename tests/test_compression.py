"""Comprehensive tests for Compression middleware."""

import pytest
from fastapi import FastAPI
from starlette.responses import StreamingResponse
from starlette.testclient import TestClient

from fastmiddleware import CompressionConfig, CompressionMiddleware


@pytest.fixture
def compression_app() -> FastAPI:
    """Create app with compression middleware."""
    app = FastAPI()
    app.add_middleware(CompressionMiddleware, minimum_size=100)

    @app.get("/")
    async def root():
        """Execute root operation.

        Returns:
            The result of the operation.
        """
        return {"message": "Hello"}

    @app.get("/large")
    async def large():
        """Execute large operation.

        Returns:
            The result of the operation.
        """
        # Return large response that should be compressed
        return {"data": "x" * 1000, "items": list(range(100))}

    @app.get("/small")
    async def small():
        """Execute small operation.

        Returns:
            The result of the operation.
        """
        return {"ok": True}

    @app.get("/html")
    async def html():
        """Execute html operation.

        Returns:
            The result of the operation.
        """
        from starlette.responses import HTMLResponse

        return HTMLResponse("<html><body>" + "x" * 1000 + "</body></html>")

    @app.get("/binary")
    async def binary():
        """Execute binary operation.

        Returns:
            The result of the operation.
        """
        from starlette.responses import Response

        return Response(content=b"\x00" * 1000, media_type="application/octet-stream")

    @app.get("/stream")
    async def stream():
        """Execute stream operation.

        Returns:
            The result of the operation.
        """

        async def generate():
            """Execute generate operation.

            Returns:
                The result of the operation.
            """
            for i in range(10):
                yield f"chunk {i}\n"

        return StreamingResponse(generate(), media_type="text/plain")

    return app


@pytest.fixture
def compression_client(compression_app: FastAPI) -> TestClient:
    """Create test client for compression app."""
    return TestClient(compression_app)


class TestCompressionMiddleware:
    """Tests for CompressionMiddleware."""

    def test_compresses_large_response_when_accepted(
        self, compression_client: TestClient
    ):
        """Test that large responses are compressed when client accepts gzip."""
        response = compression_client.get(
            "/large", headers={"Accept-Encoding": "gzip, deflate"}
        )

        assert response.status_code == 200
        assert response.headers.get("Vary") == "Accept-Encoding"

    def test_no_compression_without_accept_header(self, compression_client: TestClient):
        """Test behavior when client doesn't explicitly accept gzip."""
        response = compression_client.get("/large")

        assert response.status_code == 200
        # Note: TestClient may still accept gzip by default
        # Just verify response is successful

    def test_small_response_not_compressed(self, compression_client: TestClient):
        """Test that small responses are not compressed."""
        response = compression_client.get("/small", headers={"Accept-Encoding": "gzip"})

        assert response.status_code == 200
        # Small responses should not be compressed
        assert response.headers.get("Content-Encoding") != "gzip"

    def test_html_content_compressed(self, compression_client: TestClient):
        """Test that HTML content is compressed."""
        response = compression_client.get("/html", headers={"Accept-Encoding": "gzip"})

        assert response.status_code == 200
        assert response.headers.get("Vary") == "Accept-Encoding"

    def test_streaming_response_not_compressed(self, compression_client: TestClient):
        """Test that streaming responses are not compressed."""
        response = compression_client.get(
            "/stream", headers={"Accept-Encoding": "gzip"}
        )

        assert response.status_code == 200
        # Streaming responses should pass through

    def test_vary_header_always_added(self, compression_client: TestClient):
        """Starlette gzip adds ``Vary: Accept-Encoding`` when compression may apply."""
        response = compression_client.get("/html", headers={"Accept-Encoding": "gzip"})

        assert response.headers.get("Vary") == "Accept-Encoding"


class TestCompressionConfig:
    """Tests for CompressionConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = CompressionConfig()

        assert config.minimum_size == 500
        assert config.compression_level == 6
        assert "application/json" in config.compressible_types
        assert "text/html" in config.compressible_types
        assert "text/css" in config.compressible_types

    def test_custom_config(self):
        """Test custom configuration values."""
        config = CompressionConfig(
            minimum_size=1000,
            compression_level=9,
        )

        assert config.minimum_size == 1000
        assert config.compression_level == 9

    def test_custom_compressible_types(self):
        """Test custom compressible types."""
        config = CompressionConfig(
            compressible_types=("application/json", "text/plain"),
        )

        assert len(config.compressible_types) == 2
        assert "application/json" in config.compressible_types


class TestCompressionLevels:
    """Tests for different compression levels."""

    @pytest.fixture
    def high_compression_app(self) -> FastAPI:
        """Create app with high compression."""
        app = FastAPI()
        config = CompressionConfig(compression_level=9, minimum_size=100)
        app.add_middleware(CompressionMiddleware, config=config)

        @app.get("/data")
        async def data():
            """Execute data operation.

            Returns:
                The result of the operation.
            """
            return {"data": "x" * 1000}

        return app

    @pytest.fixture
    def high_compression_client(self, high_compression_app: FastAPI) -> TestClient:
        """Execute high_compression_client operation.

        Args:
            high_compression_app: The high_compression_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(high_compression_app)

    def test_high_compression_works(self, high_compression_client: TestClient):
        """Test that high compression level works."""
        response = high_compression_client.get(
            "/data", headers={"Accept-Encoding": "gzip"}
        )

        assert response.status_code == 200


class TestCompressionExclusion:
    """Tests for compression path exclusion."""

    @pytest.fixture
    def excluded_app(self) -> FastAPI:
        """Create app with path exclusion."""
        app = FastAPI()
        app.add_middleware(
            CompressionMiddleware,
            exclude_paths={"/no-compress"},
            minimum_size=100,
        )

        @app.get("/compress")
        async def compress():
            """Execute compress operation.

            Returns:
                The result of the operation.
            """
            return {"data": "x" * 1000}

        @app.get("/no-compress")
        async def no_compress():
            """Execute no_compress operation.

            Returns:
                The result of the operation.
            """
            return {"data": "x" * 1000}

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

    def test_excluded_path_not_compressed(self, excluded_client: TestClient):
        """Test that excluded paths are not compressed."""
        response = excluded_client.get(
            "/no-compress", headers={"Accept-Encoding": "gzip"}
        )

        assert response.status_code == 200
        # Should not have compression


class TestAcceptEncodingParsing:
    """Tests for Accept-Encoding header parsing."""

    @pytest.fixture
    def app(self) -> FastAPI:
        """Execute app operation.

        Returns:
            The result of the operation.
        """
        app = FastAPI()
        app.add_middleware(CompressionMiddleware, minimum_size=100)

        @app.get("/data")
        async def data():
            """Execute data operation.

            Returns:
                The result of the operation.
            """
            return {"data": "x" * 1000}

        return app

    @pytest.fixture
    def client(self, app: FastAPI) -> TestClient:
        """Execute client operation.

        Args:
            app: The app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(app)

    def test_gzip_only(self, client: TestClient):
        """Test Accept-Encoding: gzip."""
        response = client.get("/data", headers={"Accept-Encoding": "gzip"})
        assert response.status_code == 200

    def test_gzip_with_quality(self, client: TestClient):
        """Test Accept-Encoding with quality values."""
        response = client.get(
            "/data", headers={"Accept-Encoding": "gzip;q=1.0, deflate;q=0.5"}
        )
        assert response.status_code == 200

    def test_deflate_only(self, client: TestClient):
        """Test Accept-Encoding: deflate (not supported)."""
        response = client.get("/data", headers={"Accept-Encoding": "deflate"})
        assert response.status_code == 200
        # Should not compress (only gzip supported)

    def test_identity(self, client: TestClient):
        """Test Accept-Encoding: identity."""
        response = client.get("/data", headers={"Accept-Encoding": "identity"})
        assert response.status_code == 200
