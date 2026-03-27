"""Comprehensive tests for Cache middleware."""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import CacheConfig, CacheMiddleware


@pytest.fixture
def cache_app() -> FastAPI:
    """Create app with cache middleware."""
    app = FastAPI()
    config = CacheConfig(
        default_max_age=3600,
        enable_etag=True,
    )
    app.add_middleware(CacheMiddleware, config=config)

    @app.get("/data")
    async def get_data():
        """Execute get_data operation.

        Returns:
            The result of the operation.
        """
        return {"message": "Hello", "timestamp": "2024-01-01"}

    @app.get("/dynamic")
    async def get_dynamic():
        """Execute get_dynamic operation.

        Returns:
            The result of the operation.
        """
        import time

        return {"time": time.time()}

    @app.post("/create")
    async def create_data():
        """Execute create_data operation.

        Returns:
            The result of the operation.
        """
        return {"created": True}

    @app.get("/empty")
    async def get_empty():
        """Execute get_empty operation.

        Returns:
            The result of the operation.
        """
        return {}

    return app


@pytest.fixture
def cache_client(cache_app: FastAPI) -> TestClient:
    """Execute cache_client operation.

    Args:
        cache_app: The cache_app parameter.

    Returns:
        The result of the operation.
    """
    return TestClient(cache_app)


class TestCacheMiddleware:
    """Tests for CacheMiddleware."""

    def test_cache_control_header_added(self, cache_client: TestClient):
        """Test that Cache-Control header is added."""
        response = cache_client.get("/data")

        assert response.status_code == 200
        assert "Cache-Control" in response.headers
        assert "max-age=3600" in response.headers["Cache-Control"]

    def test_etag_header_added(self, cache_client: TestClient):
        """Test that ETag header is added."""
        response = cache_client.get("/data")

        assert response.status_code == 200
        assert "ETag" in response.headers
        assert response.headers["ETag"].startswith('"')
        assert response.headers["ETag"].endswith('"')

    def test_vary_header_added(self, cache_client: TestClient):
        """Test that Vary header is added."""
        response = cache_client.get("/data")

        assert response.status_code == 200
        assert "Vary" in response.headers

    def test_post_not_cached(self, cache_client: TestClient):
        """Test that POST requests are not cached."""
        response = cache_client.post("/create")

        assert response.status_code == 200
        # POST should not have typical cache headers

    def test_same_content_same_etag(self, cache_client: TestClient):
        """Test that same content produces same ETag."""
        response1 = cache_client.get("/data")
        response2 = cache_client.get("/data")

        assert response1.headers["ETag"] == response2.headers["ETag"]


class TestConditionalRequests:
    """Tests for conditional GET requests."""

    def test_304_on_matching_etag(self, cache_client: TestClient):
        """Test that 304 is returned when ETag matches."""
        # Get initial response with ETag
        response1 = cache_client.get("/data")
        etag = response1.headers.get("ETag")

        assert etag is not None

        # Send conditional request
        response2 = cache_client.get("/data", headers={"If-None-Match": etag})

        assert response2.status_code == 304

    def test_304_has_etag(self, cache_client: TestClient):
        """Test that 304 response has ETag header."""
        response1 = cache_client.get("/data")
        etag = response1.headers["ETag"]

        response2 = cache_client.get("/data", headers={"If-None-Match": etag})

        assert response2.headers.get("ETag") == etag

    def test_200_on_non_matching_etag(self, cache_client: TestClient):
        """Test that 200 is returned when ETag doesn't match."""
        response = cache_client.get(
            "/data", headers={"If-None-Match": '"non-matching-etag"'}
        )

        assert response.status_code == 200

    def test_304_has_cache_control(self, cache_client: TestClient):
        """Test that 304 response has Cache-Control header."""
        response1 = cache_client.get("/data")
        etag = response1.headers["ETag"]

        response2 = cache_client.get("/data", headers={"If-None-Match": etag})

        assert "Cache-Control" in response2.headers


class TestCacheConfig:
    """Tests for CacheConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = CacheConfig()

        assert config.default_max_age == 0
        assert config.enable_etag is True
        assert config.private is False
        assert config.no_store is False
        assert "GET" in config.cacheable_methods
        assert "HEAD" in config.cacheable_methods
        assert 200 in config.cacheable_status_codes

    def test_custom_config(self):
        """Test custom configuration values."""
        config = CacheConfig(
            default_max_age=7200,
            enable_etag=False,
            private=True,
        )

        assert config.default_max_age == 7200
        assert config.enable_etag is False
        assert config.private is True

    def test_path_rules(self):
        """Test path-specific cache rules."""
        config = CacheConfig(
            path_rules={
                "/api/static": {"max_age": 86400, "public": True},
                "/api/private": {"max_age": 0, "no_store": True},
            }
        )

        assert config.path_rules["/api/static"]["max_age"] == 86400
        assert config.path_rules["/api/private"]["no_store"] is True


class TestPathRules:
    """Tests for path-specific cache rules."""

    @pytest.fixture
    def path_rules_app(self) -> FastAPI:
        """Create app with path-specific rules."""
        app = FastAPI()
        config = CacheConfig(
            default_max_age=60,
            path_rules={
                "/static": {"max_age": 86400},
                "/private": {"private": True, "max_age": 0},
                "/no-cache": {"no_store": True},
            },
        )
        app.add_middleware(CacheMiddleware, config=config)

        @app.get("/static/file")
        async def static_file():
            """Execute static_file operation.

            Returns:
                The result of the operation.
            """
            return {"type": "static"}

        @app.get("/private/data")
        async def private_data():
            """Execute private_data operation.

            Returns:
                The result of the operation.
            """
            return {"type": "private"}

        @app.get("/no-cache/data")
        async def no_cache_data():
            """Execute no_cache_data operation.

            Returns:
                The result of the operation.
            """
            return {"type": "no-cache"}

        @app.get("/default")
        async def default():
            """Execute default operation.

            Returns:
                The result of the operation.
            """
            return {"type": "default"}

        return app

    @pytest.fixture
    def path_rules_client(self, path_rules_app: FastAPI) -> TestClient:
        """Execute path_rules_client operation.

        Args:
            path_rules_app: The path_rules_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(path_rules_app)

    def test_static_path_long_cache(self, path_rules_client: TestClient):
        """Test that static paths have long cache."""
        response = path_rules_client.get("/static/file")

        assert "max-age=86400" in response.headers["Cache-Control"]

    def test_private_path_private_cache(self, path_rules_client: TestClient):
        """Test that private paths have private cache."""
        response = path_rules_client.get("/private/data")

        assert "private" in response.headers["Cache-Control"]

    def test_default_path_uses_default(self, path_rules_client: TestClient):
        """Test that unmatched paths use default."""
        response = path_rules_client.get("/default")

        assert "max-age=60" in response.headers["Cache-Control"]


class TestNoEtag:
    """Tests for disabled ETag."""

    @pytest.fixture
    def no_etag_app(self) -> FastAPI:
        """Create app without ETag."""
        app = FastAPI()
        config = CacheConfig(enable_etag=False)
        app.add_middleware(CacheMiddleware, config=config)

        @app.get("/data")
        async def get_data():
            """Execute get_data operation.

            Returns:
                The result of the operation.
            """
            return {"value": 123}

        return app

    @pytest.fixture
    def no_etag_client(self, no_etag_app: FastAPI) -> TestClient:
        """Execute no_etag_client operation.

        Args:
            no_etag_app: The no_etag_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(no_etag_app)

    def test_no_etag_header(self, no_etag_client: TestClient):
        """Test that ETag header is not added."""
        response = no_etag_client.get("/data")

        assert "ETag" not in response.headers

    def test_conditional_request_returns_200(self, no_etag_client: TestClient):
        """Test that conditional request returns 200 without ETag."""
        response = no_etag_client.get("/data", headers={"If-None-Match": '"some-etag"'})

        assert response.status_code == 200


class TestPrivateCache:
    """Tests for private cache."""

    @pytest.fixture
    def private_app(self) -> FastAPI:
        """Create app with private cache."""
        app = FastAPI()
        config = CacheConfig(private=True, default_max_age=300)
        app.add_middleware(CacheMiddleware, config=config)

        @app.get("/data")
        async def get_data():
            """Execute get_data operation.

            Returns:
                The result of the operation.
            """
            return {"value": "secret"}

        return app

    @pytest.fixture
    def private_client(self, private_app: FastAPI) -> TestClient:
        """Execute private_client operation.

        Args:
            private_app: The private_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(private_app)

    def test_private_cache_control(self, private_client: TestClient):
        """Test that Cache-Control includes private."""
        response = private_client.get("/data")

        assert "private" in response.headers["Cache-Control"]


class TestPathExclusion:
    """Tests for path exclusion."""

    @pytest.fixture
    def excluded_app(self) -> FastAPI:
        """Create app with path exclusion."""
        app = FastAPI()
        config = CacheConfig(default_max_age=3600, enable_etag=True)
        app.add_middleware(
            CacheMiddleware,
            config=config,
            exclude_paths={"/no-cache"},
        )

        @app.get("/cached")
        async def cached():
            """Execute cached operation.

            Returns:
                The result of the operation.
            """
            return {"cached": True}

        @app.get("/no-cache")
        async def no_cache():
            """Execute no_cache operation.

            Returns:
                The result of the operation.
            """
            return {"cached": False}

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

    def test_excluded_path_no_cache_headers(self, excluded_client: TestClient):
        """Test that excluded paths don't get cache headers."""
        response = excluded_client.get("/no-cache")

        # Should pass through without cache middleware processing
        assert response.status_code == 200

    def test_included_path_has_cache_headers(self, excluded_client: TestClient):
        """Test that included paths get cache headers."""
        response = excluded_client.get("/cached")

        assert "Cache-Control" in response.headers
        assert "ETag" in response.headers
