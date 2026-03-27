"""Comprehensive tests for Idempotency middleware."""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmiddleware import (
    IdempotencyConfig,
    IdempotencyMiddleware,
    InMemoryIdempotencyStore,
)


@pytest.fixture
def idempotency_app() -> FastAPI:
    """Create app with idempotency middleware."""
    app = FastAPI()
    app.add_middleware(IdempotencyMiddleware)

    counter = {"value": 0}

    @app.post("/create")
    async def create():
        """Execute create operation.

        Returns:
            The result of the operation.
        """
        counter["value"] += 1
        return {"created": True, "count": counter["value"]}

    @app.put("/update")
    async def update():
        """Execute update operation.

        Returns:
            The result of the operation.
        """
        counter["value"] += 1
        return {"updated": True, "count": counter["value"]}

    @app.patch("/patch")
    async def patch():
        """Execute patch operation.

        Returns:
            The result of the operation.
        """
        counter["value"] += 1
        return {"patched": True, "count": counter["value"]}

    @app.get("/read")
    async def read():
        """Execute read operation.

        Returns:
            The result of the operation.
        """
        return {"count": counter["value"]}

    @app.delete("/delete")
    async def delete():
        """Execute delete operation.

        Returns:
            The result of the operation.
        """
        return {"deleted": True}

    return app


@pytest.fixture
def idempotency_client(idempotency_app: FastAPI) -> TestClient:
    """Execute idempotency_client operation.

    Args:
        idempotency_app: The idempotency_app parameter.

    Returns:
        The result of the operation.
    """
    return TestClient(idempotency_app)


class TestIdempotencyMiddleware:
    """Tests for IdempotencyMiddleware."""

    def test_post_with_key_is_cached(self, idempotency_client: TestClient):
        """Test that POST requests with idempotency key are cached."""
        key = "unique-key-123"

        # First request
        response1 = idempotency_client.post("/create", headers={"Idempotency-Key": key})
        assert response1.status_code == 200
        count1 = response1.json()["count"]

        # Second request with same key (should return cached)
        response2 = idempotency_client.post("/create", headers={"Idempotency-Key": key})
        assert response2.status_code == 200
        assert response2.json()["count"] == count1  # Same as first request
        assert response2.headers.get("X-Idempotent-Replayed") == "true"

    def test_put_with_key_is_cached(self, idempotency_client: TestClient):
        """Test that PUT requests with idempotency key are cached."""
        key = "put-key-456"

        response1 = idempotency_client.put("/update", headers={"Idempotency-Key": key})
        response2 = idempotency_client.put("/update", headers={"Idempotency-Key": key})

        assert response1.json()["count"] == response2.json()["count"]
        assert response2.headers.get("X-Idempotent-Replayed") == "true"

    def test_patch_with_key_is_cached(self, idempotency_client: TestClient):
        """Test that PATCH requests with idempotency key are cached."""
        key = "patch-key-789"

        response1 = idempotency_client.patch("/patch", headers={"Idempotency-Key": key})
        response2 = idempotency_client.patch("/patch", headers={"Idempotency-Key": key})

        assert response1.json()["count"] == response2.json()["count"]

    def test_different_keys_not_cached(self, idempotency_client: TestClient):
        """Test that different keys produce different responses."""
        response1 = idempotency_client.post(
            "/create", headers={"Idempotency-Key": "key-1"}
        )
        response2 = idempotency_client.post(
            "/create", headers={"Idempotency-Key": "key-2"}
        )

        assert response1.json()["count"] != response2.json()["count"]

    def test_get_requests_not_affected(self, idempotency_client: TestClient):
        """Test that GET requests are not affected by idempotency."""
        response = idempotency_client.get("/read")
        assert response.status_code == 200
        assert "X-Idempotent-Replayed" not in response.headers

    def test_request_without_key_not_cached(self, idempotency_client: TestClient):
        """Test that requests without key are not cached."""
        response1 = idempotency_client.post("/create")
        response2 = idempotency_client.post("/create")

        # Both should execute (different counts)
        assert response1.json()["count"] != response2.json()["count"]

    def test_no_replay_header_on_first_request(self, idempotency_client: TestClient):
        """Test that first request doesn't have replay header."""
        response = idempotency_client.post(
            "/create", headers={"Idempotency-Key": "first-time-key"}
        )

        assert "X-Idempotent-Replayed" not in response.headers


class TestIdempotencyConfig:
    """Tests for IdempotencyConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = IdempotencyConfig()

        assert config.header_name == "Idempotency-Key"
        assert config.ttl_seconds == 86400
        assert "POST" in config.required_methods
        assert "PUT" in config.required_methods
        assert "PATCH" in config.required_methods
        assert config.require_key is False

    def test_custom_config(self):
        """Test custom configuration values."""
        config = IdempotencyConfig(
            header_name="X-Idempotency-Key",
            ttl_seconds=3600,
            require_key=True,
        )

        assert config.header_name == "X-Idempotency-Key"
        assert config.ttl_seconds == 3600
        assert config.require_key is True

    def test_custom_required_methods(self):
        """Test custom required methods."""
        config = IdempotencyConfig(
            required_methods={"POST"},
        )

        assert "POST" in config.required_methods
        assert "PUT" not in config.required_methods


class TestRequiredKey:
    """Tests for required idempotency key."""

    @pytest.fixture
    def required_key_app(self) -> FastAPI:
        """Create app with required idempotency key."""
        app = FastAPI()
        config = IdempotencyConfig(require_key=True)
        app.add_middleware(IdempotencyMiddleware, config=config)

        @app.post("/create")
        async def create():
            """Execute create operation.

            Returns:
                The result of the operation.
            """
            return {"created": True}

        @app.get("/read")
        async def read():
            """Execute read operation.

            Returns:
                The result of the operation.
            """
            return {"data": "value"}

        return app

    @pytest.fixture
    def required_key_client(self, required_key_app: FastAPI) -> TestClient:
        """Execute required_key_client operation.

        Args:
            required_key_app: The required_key_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(required_key_app)

    def test_missing_key_returns_400(self, required_key_client: TestClient):
        """Test that missing key returns error when required."""
        response = required_key_client.post("/create")

        assert response.status_code == 400
        assert "Missing" in response.json()["message"]

    def test_with_key_succeeds(self, required_key_client: TestClient):
        """Test that request with key succeeds."""
        response = required_key_client.post(
            "/create", headers={"Idempotency-Key": "my-key"}
        )

        assert response.status_code == 200

    def test_get_not_affected(self, required_key_client: TestClient):
        """Test that GET requests don't require key."""
        response = required_key_client.get("/read")

        assert response.status_code == 200


class TestCustomHeader:
    """Tests for custom header name."""

    @pytest.fixture
    def custom_header_app(self) -> FastAPI:
        """Create app with custom header name."""
        app = FastAPI()
        config = IdempotencyConfig(header_name="X-Custom-Key")
        app.add_middleware(IdempotencyMiddleware, config=config)

        counter = {"value": 0}

        @app.post("/create")
        async def create():
            """Execute create operation.

            Returns:
                The result of the operation.
            """
            counter["value"] += 1
            return {"count": counter["value"]}

        return app

    @pytest.fixture
    def custom_header_client(self, custom_header_app: FastAPI) -> TestClient:
        """Execute custom_header_client operation.

        Args:
            custom_header_app: The custom_header_app parameter.

        Returns:
            The result of the operation.
        """
        return TestClient(custom_header_app)

    def test_custom_header_works(self, custom_header_client: TestClient):
        """Test that custom header name works."""
        key = "custom-key"

        response1 = custom_header_client.post("/create", headers={"X-Custom-Key": key})
        response2 = custom_header_client.post("/create", headers={"X-Custom-Key": key})

        assert response1.json()["count"] == response2.json()["count"]

    def test_standard_header_not_used(self, custom_header_client: TestClient):
        """Test that standard header is not used."""
        key = "standard-key"

        response1 = custom_header_client.post(
            "/create", headers={"Idempotency-Key": key}
        )
        response2 = custom_header_client.post(
            "/create", headers={"Idempotency-Key": key}
        )

        # Should not be cached (different counts)
        assert response1.json()["count"] != response2.json()["count"]


class TestInMemoryIdempotencyStore:
    """Tests for InMemoryIdempotencyStore."""

    @pytest.mark.asyncio
    async def test_set_and_get(self):
        """Test storing and retrieving data."""
        store = InMemoryIdempotencyStore()

        await store.set("key1", {"data": "test"}, ttl=60)
        result = await store.get("key1")

        assert result == {"data": "test"}

    @pytest.mark.asyncio
    async def test_missing_key_returns_none(self):
        """Test that missing key returns None."""
        store = InMemoryIdempotencyStore()

        result = await store.get("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_delete(self):
        """Test deleting data."""
        store = InMemoryIdempotencyStore()

        await store.set("key1", {"data": "test"}, ttl=60)
        await store.delete("key1")
        result = await store.get("key1")

        assert result is None

    @pytest.mark.asyncio
    async def test_multiple_keys(self):
        """Test storing multiple keys."""
        store = InMemoryIdempotencyStore()

        await store.set("key1", {"value": 1}, ttl=60)
        await store.set("key2", {"value": 2}, ttl=60)
        await store.set("key3", {"value": 3}, ttl=60)

        assert (await store.get("key1"))["value"] == 1
        assert (await store.get("key2"))["value"] == 2
        assert (await store.get("key3"))["value"] == 3

    @pytest.mark.asyncio
    async def test_overwrite_key(self):
        """Test overwriting a key."""
        store = InMemoryIdempotencyStore()

        await store.set("key1", {"value": 1}, ttl=60)
        await store.set("key1", {"value": 2}, ttl=60)

        result = await store.get("key1")
        assert result["value"] == 2


class TestPathExclusion:
    """Tests for path exclusion."""

    @pytest.fixture
    def excluded_app(self) -> FastAPI:
        """Create app with path exclusion."""
        app = FastAPI()
        config = IdempotencyConfig(require_key=True)
        app.add_middleware(
            IdempotencyMiddleware,
            config=config,
            exclude_paths={"/excluded"},
        )

        @app.post("/included")
        async def included():
            """Execute included operation.

            Returns:
                The result of the operation.
            """
            return {"ok": True}

        @app.post("/excluded")
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

    def test_excluded_path_no_key_required(self, excluded_client: TestClient):
        """Test that excluded paths don't require key."""
        response = excluded_client.post("/excluded")

        assert response.status_code == 200

    def test_included_path_requires_key(self, excluded_client: TestClient):
        """Test that included paths require key."""
        response = excluded_client.post("/included")

        assert response.status_code == 400
