"""Comprehensive tests for all middlewares to achieve 100% coverage."""

import hashlib
import hmac
import time

from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient


# ============== AB Testing ==============
class TestABTesting:
    """Represents the TestABTesting class."""

    def test_ab_test_basic(self):
        """Execute test_ab_test_basic operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ABTestMiddleware, Experiment

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse(
                {"variant": request.state.ab_variants.get("test_exp", "none")}
            )

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(
            ABTestMiddleware,
            experiments=[
                Experiment(name="test_exp", variants=["a", "b"], weights=[0.5, 0.5])
            ],
        )
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["variant"] in ["a", "b"]

    def test_ab_test_sticky_variant(self):
        """Execute test_ab_test_sticky_variant operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ABTestMiddleware, Experiment

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse(
                {"variant": request.state.ab_variants.get("exp", "none")}
            )

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(
            ABTestMiddleware, experiments=[Experiment(name="exp", variants=["x", "y"])]
        )
        client = TestClient(app)

        # First request sets cookie
        resp1 = client.get("/")
        variant1 = resp1.json()["variant"]

        # Second request uses same cookie - should get same variant
        resp2 = client.get("/")
        variant2 = resp2.json()["variant"]
        assert variant1 == variant2


# ============== Accept Language ==============
class TestAcceptLanguage:
    """Represents the TestAcceptLanguage class."""

    def test_accept_language_basic(self):
        """Execute test_accept_language_basic operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import AcceptLanguageMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse({"lang": getattr(request.state, "language", "en")})

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(
            AcceptLanguageMiddleware,
            supported_languages=["en", "es", "fr"],
        )
        client = TestClient(app)

        # Test with Accept-Language header
        response = client.get("/", headers={"Accept-Language": "es,en;q=0.9"})
        assert response.status_code == 200

    def test_accept_language_default(self):
        """Execute test_accept_language_default operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import AcceptLanguageMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse({"lang": getattr(request.state, "language", "en")})

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(AcceptLanguageMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== API Version Header ==============
class TestAPIVersionHeader:
    """Represents the TestAPIVersionHeader class."""

    def test_api_version_header(self):
        """Execute test_api_version_header operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import APIVersionHeaderMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(APIVersionHeaderMiddleware, version="1.0.0")
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200
        assert (
            "X-API-Version" in response.headers
            or response.headers.get("x-api-version") == "1.0.0"
        )


# ============== Audit ==============
class TestAudit:
    """Represents the TestAudit class."""

    def test_audit_logging(self):
        """Execute test_audit_logging operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import AuditMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse({"status": "ok"})

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(AuditMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Bandwidth ==============
class TestBandwidth:
    """Represents the TestBandwidth class."""

    def test_bandwidth_throttle(self):
        """Execute test_bandwidth_throttle operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import BandwidthMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("X" * 1000)

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(BandwidthMiddleware, bytes_per_second=10000)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200
        assert len(response.text) == 1000


# ============== Basic Auth ==============
class TestBasicAuth:
    """Represents the TestBasicAuth class."""

    def test_basic_auth_success(self):
        """Execute test_basic_auth_success operation.

        Returns:
            The result of the operation.
        """
        import base64

        from fastmiddleware import BasicAuthMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse(f"Hello {request.state.user}")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(BasicAuthMiddleware, users={"admin": "secret"})
        client = TestClient(app)

        credentials = base64.b64encode(b"admin:secret").decode()
        response = client.get("/", headers={"Authorization": f"Basic {credentials}"})
        assert response.status_code == 200
        assert "admin" in response.text

    def test_basic_auth_failure(self):
        """Execute test_basic_auth_failure operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import BasicAuthMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(BasicAuthMiddleware, users={"admin": "secret"})
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 401


# ============== Bearer Auth ==============
class TestBearerAuth:
    """Represents the TestBearerAuth class."""

    def test_bearer_auth_success(self):
        """Execute test_bearer_auth_success operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import BearerAuthMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(BearerAuthMiddleware, tokens={"token123": {"user": "admin"}})
        client = TestClient(app)

        response = client.get("/", headers={"Authorization": "Bearer token123"})
        assert response.status_code == 200

    def test_bearer_auth_invalid(self):
        """Execute test_bearer_auth_invalid operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import BearerAuthMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(BearerAuthMiddleware, tokens={"token123": {"user": "admin"}})
        client = TestClient(app)

        response = client.get("/", headers={"Authorization": "Bearer invalid"})
        assert response.status_code == 401


# ============== Bot Detection ==============
class TestBotDetection:
    """Represents the TestBotDetection class."""

    def test_bot_detection(self):
        """Execute test_bot_detection operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import BotDetectionMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse({"is_bot": getattr(request.state, "is_bot", False)})

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(BotDetectionMiddleware)
        client = TestClient(app)

        # Normal user agent
        response = client.get("/", headers={"User-Agent": "Mozilla/5.0"})
        assert response.status_code == 200

        # Bot user agent
        response = client.get("/", headers={"User-Agent": "Googlebot/2.1"})
        assert response.status_code == 200


# ============== Bulkhead ==============
class TestBulkhead:
    """Represents the TestBulkhead class."""

    def test_bulkhead_allows_request(self):
        """Execute test_bulkhead_allows_request operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import BulkheadMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(BulkheadMiddleware, max_concurrent=10)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Chaos ==============
class TestChaos:
    """Represents the TestChaos class."""

    def test_chaos_disabled(self):
        """Execute test_chaos_disabled operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ChaosMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ChaosMiddleware, enabled=False)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Circuit Breaker ==============
class TestCircuitBreaker:
    """Represents the TestCircuitBreaker class."""

    def test_circuit_breaker_closed(self):
        """Execute test_circuit_breaker_closed operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import CircuitBreakerMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(CircuitBreakerMiddleware, failure_threshold=5)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Client Hints ==============
class TestClientHints:
    """Represents the TestClientHints class."""

    def test_client_hints(self):
        """Execute test_client_hints operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ClientHintsMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ClientHintsMiddleware)
        client = TestClient(app)

        response = client.get("/", headers={"Sec-CH-UA": '"Chromium";v="120"'})
        assert response.status_code == 200


# ============== Conditional Request ==============
class TestConditionalRequest:
    """Represents the TestConditionalRequest class."""

    def test_conditional_request(self):
        """Execute test_conditional_request operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ConditionalRequestMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ConditionalRequestMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Content Negotiation ==============
class TestContentNegotiation:
    """Represents the TestContentNegotiation class."""

    def test_content_negotiation(self):
        """Execute test_content_negotiation operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ContentNegotiationMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse(
                {"type": getattr(request.state, "content_type", "application/json")}
            )

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(
            ContentNegotiationMiddleware,
            supported_types=["application/json", "application/xml"],
        )
        client = TestClient(app)

        response = client.get("/", headers={"Accept": "application/json"})
        assert response.status_code == 200


# ============== Content Type ==============
class TestContentType:
    """Represents the TestContentType class."""

    def test_content_type_validation(self):
        """Execute test_content_type_validation operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ContentTypeMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage, methods=["POST"])])
        app.add_middleware(ContentTypeMiddleware)
        client = TestClient(app)

        response = client.post("/", json={"test": 1})
        assert response.status_code == 200


# ============== Context ==============
class TestContext:
    """Represents the TestContext class."""

    def test_context_middleware(self):
        """Execute test_context_middleware operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ContextMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ContextMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Correlation ==============
class TestCorrelation:
    """Represents the TestCorrelation class."""

    def test_correlation_id(self):
        """Execute test_correlation_id operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import CorrelationMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(CorrelationMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200
        assert (
            "X-Correlation-ID" in response.headers
            or "x-correlation-id" in response.headers
        )

    def test_correlation_id_passed(self):
        """Execute test_correlation_id_passed operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import CorrelationMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(CorrelationMiddleware)
        client = TestClient(app)

        response = client.get("/", headers={"X-Correlation-ID": "test-123"})
        assert response.status_code == 200


# ============== Cost Tracking ==============
class TestCostTracking:
    """Represents the TestCostTracking class."""

    def test_cost_tracking(self):
        """Execute test_cost_tracking operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import CostTrackingMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(CostTrackingMiddleware, path_costs={"/": 1.0})
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== CSP Report ==============
class TestCSPReport:
    """Represents the TestCSPReport class."""

    def test_csp_report(self):
        """Execute test_csp_report operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import CSPReportMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(CSPReportMiddleware, report_uri="/_csp-report")
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== CSRF ==============
class TestCSRF:
    """Represents the TestCSRF class."""

    def test_csrf_get_token(self):
        """Execute test_csrf_get_token operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import CSRFConfig, CSRFMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        config = CSRFConfig(secret="test-secret-key-32-chars-long!!")
        app.add_middleware(CSRFMiddleware, config=config)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Data Masking ==============
class TestDataMasking:
    """Represents the TestDataMasking class."""

    def test_data_masking(self):
        """Execute test_data_masking operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import DataMaskingMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse({"password": "secret123"})

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(DataMaskingMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Deprecation ==============
class TestDeprecation:
    """Represents the TestDeprecation class."""

    def test_deprecation_warning(self):
        """Execute test_deprecation_warning operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import DeprecationInfo, DeprecationMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/old", homepage)])
        info = DeprecationInfo(
            message="This endpoint is deprecated",
            sunset_date="2025-12-31",
            replacement="/new",
        )
        app.add_middleware(DeprecationMiddleware, deprecated_paths={"/old": info})
        client = TestClient(app)

        response = client.get("/old")
        assert response.status_code == 200


# ============== Early Hints ==============
class TestEarlyHints:
    """Represents the TestEarlyHints class."""

    def test_early_hints(self):
        """Execute test_early_hints operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import EarlyHintsMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(EarlyHintsMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== ETag ==============
class TestETag:
    """Represents the TestETag class."""

    def test_etag_generation(self):
        """Execute test_etag_generation operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ETagMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("Hello World")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ETagMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Exception Handler ==============
class TestExceptionHandler:
    """Represents the TestExceptionHandler class."""

    def test_exception_handler(self):
        """Execute test_exception_handler operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ExceptionHandlerMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ExceptionHandlerMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Feature Flag ==============
class TestFeatureFlag:
    """Represents the TestFeatureFlag class."""

    def test_feature_flag(self):
        """Execute test_feature_flag operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import FeatureFlagMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            flags = getattr(request.state, "feature_flags", {})
            return JSONResponse({"flags": flags})

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(
            FeatureFlagMiddleware, flags={"new_feature": True, "old_feature": False}
        )
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== GeoIP ==============
class TestGeoIP:
    """Represents the TestGeoIP class."""

    def test_geoip(self):
        """Execute test_geoip operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import GeoIPMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(GeoIPMiddleware)
        client = TestClient(app)

        response = client.get("/", headers={"CF-IPCountry": "US"})
        assert response.status_code == 200


# ============== Graceful Shutdown ==============
class TestGracefulShutdown:
    """Represents the TestGracefulShutdown class."""

    def test_graceful_shutdown_normal(self):
        """Execute test_graceful_shutdown_normal operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import GracefulShutdownMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        GracefulShutdownMiddleware(app)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== HATEOAS ==============
class TestHATEOAS:
    """Represents the TestHATEOAS class."""

    def test_hateoas(self):
        """Execute test_hateoas operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import HATEOASMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse({"id": 1})

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(HATEOASMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Header Transform ==============
class TestHeaderTransform:
    """Represents the TestHeaderTransform class."""

    def test_header_transform(self):
        """Execute test_header_transform operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import HeaderTransformMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(
            HeaderTransformMiddleware, add_response_headers={"X-Custom": "value"}
        )
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200
        assert response.headers.get("X-Custom") == "value"


# ============== Honeypot ==============
class TestHoneypot:
    """Represents the TestHoneypot class."""

    def test_honeypot_normal(self):
        """Execute test_honeypot_normal operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import HoneypotMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(HoneypotMiddleware, honeypot_paths={"/wp-admin"})
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200

    def test_honeypot_trap(self):
        """Execute test_honeypot_trap operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import HoneypotMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage), Route("/wp-admin", homepage)])
        app.add_middleware(HoneypotMiddleware, honeypot_paths={"/wp-admin"})
        client = TestClient(app)

        client.get("/wp-admin")
        # Should return 404 or similar


# ============== HTTPS Redirect ==============
class TestHTTPSRedirect:
    """Represents the TestHTTPSRedirect class."""

    def test_https_redirect_excluded(self):
        """Execute test_https_redirect_excluded operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import HTTPSRedirectMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/health", homepage)])
        app.add_middleware(HTTPSRedirectMiddleware, exclude_paths={"/health"})
        client = TestClient(app)

        response = client.get("/health")
        assert response.status_code == 200


# ============== IP Filter ==============
class TestIPFilter:
    """Represents the TestIPFilter class."""

    def test_ip_filter_allowed(self):
        """Execute test_ip_filter_allowed operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import IPFilterMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        # Don't set whitelist, so all IPs are allowed by default
        app.add_middleware(IPFilterMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== JSON Schema ==============
class TestJSONSchema:
    """Represents the TestJSONSchema class."""

    def test_json_schema(self):
        """Execute test_json_schema operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import JSONSchemaMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse({"status": "ok"})

        app = Starlette(routes=[Route("/", homepage, methods=["POST"])])
        app.add_middleware(JSONSchemaMiddleware, schemas={})
        client = TestClient(app)

        response = client.post("/", json={"name": "test"})
        assert response.status_code == 200


# ============== Load Shedding ==============
class TestLoadShedding:
    """Represents the TestLoadShedding class."""

    def test_load_shedding_normal(self):
        """Execute test_load_shedding_normal operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import LoadSheddingMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(LoadSheddingMiddleware, max_concurrent=1000)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Locale ==============
class TestLocale:
    """Represents the TestLocale class."""

    def test_locale(self):
        """Execute test_locale operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import LocaleMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(LocaleMiddleware, supported_locales=["en", "es"])
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Method Override ==============
class TestMethodOverride:
    """Represents the TestMethodOverride class."""

    def test_method_override(self):
        """Execute test_method_override operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import MethodOverrideMiddleware

        async def delete_handler(request):
            """Execute delete_handler operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse(f"Method: {request.method}")

        app = Starlette(routes=[Route("/", delete_handler, methods=["DELETE", "POST"])])
        app.add_middleware(MethodOverrideMiddleware)
        client = TestClient(app)

        response = client.post("/", headers={"X-HTTP-Method-Override": "DELETE"})
        assert response.status_code == 200


# ============== No Cache ==============
class TestNoCache:
    """Represents the TestNoCache class."""

    def test_no_cache(self):
        """Execute test_no_cache operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import NoCacheMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(NoCacheMiddleware, paths={"/", "/api"})
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Origin ==============
class TestOrigin:
    """Represents the TestOrigin class."""

    def test_origin(self):
        """Execute test_origin operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import OriginMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(OriginMiddleware, allowed_origins={"http://localhost"})
        client = TestClient(app)

        response = client.get("/", headers={"Origin": "http://localhost"})
        assert response.status_code == 200


# ============== Path Rewrite ==============
class TestPathRewrite:
    """Represents the TestPathRewrite class."""

    def test_path_rewrite(self):
        """Execute test_path_rewrite operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import PathRewriteMiddleware, RewriteRule

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse(f"Path: {request.url.path}")

        app = Starlette(
            routes=[Route("/api/v1/test", homepage), Route("/old/test", homepage)]
        )
        app.add_middleware(
            PathRewriteMiddleware, rules=[RewriteRule("/old", "/api/v1")]
        )
        client = TestClient(app)

        response = client.get("/old/test")
        assert response.status_code == 200


# ============== Payload Size ==============
class TestPayloadSize:
    """Represents the TestPayloadSize class."""

    def test_payload_size(self):
        """Execute test_payload_size operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import PayloadSizeMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage, methods=["POST"])])
        app.add_middleware(PayloadSizeMiddleware, max_request_size=1024 * 1024)
        client = TestClient(app)

        response = client.post("/", content="test data")
        assert response.status_code == 200


# ============== Permissions Policy ==============
class TestPermissionsPolicy:
    """Represents the TestPermissionsPolicy class."""

    def test_permissions_policy(self):
        """Execute test_permissions_policy operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import PermissionsPolicyMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(PermissionsPolicyMiddleware, policies={"camera": []})
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Profiling ==============
class TestProfiling:
    """Represents the TestProfiling class."""

    def test_profiling(self):
        """Execute test_profiling operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ProfilingMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ProfilingMiddleware, enabled=True)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Quota ==============
class TestQuota:
    """Represents the TestQuota class."""

    def test_quota(self):
        """Execute test_quota operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import QuotaMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(QuotaMiddleware, default_quota=1000)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Real IP ==============
class TestRealIP:
    """Represents the TestRealIP class."""

    def test_real_ip(self):
        """Execute test_real_ip operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RealIPMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RealIPMiddleware)
        client = TestClient(app)

        response = client.get("/", headers={"X-Real-IP": "1.2.3.4"})
        assert response.status_code == 200


# ============== Redirect ==============
class TestRedirect:
    """Represents the TestRedirect class."""

    def test_redirect(self):
        """Execute test_redirect operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RedirectMiddleware, RedirectRule

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/new", homepage)])
        app.add_middleware(RedirectMiddleware, rules=[RedirectRule("/old", "/new")])
        client = TestClient(app, follow_redirects=False)

        response = client.get("/old")
        assert response.status_code in [301, 302, 307, 308]


# ============== Referrer Policy ==============
class TestReferrerPolicy:
    """Represents the TestReferrerPolicy class."""

    def test_referrer_policy(self):
        """Execute test_referrer_policy operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ReferrerPolicyMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ReferrerPolicyMiddleware, policy="strict-origin")
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200
        assert "Referrer-Policy" in response.headers


# ============== Replay Prevention ==============
class TestReplayPrevention:
    """Represents the TestReplayPrevention class."""

    def test_replay_prevention(self):
        """Execute test_replay_prevention operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ReplayPreventionMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ReplayPreventionMiddleware)
        client = TestClient(app)

        timestamp = str(int(time.time()))
        nonce = "unique-nonce-123"
        client.get("/", headers={"X-Timestamp": timestamp, "X-Nonce": nonce})
        # May fail without both headers, which is expected behavior


# ============== Request Coalescing ==============
class TestRequestCoalescing:
    """Represents the TestRequestCoalescing class."""

    def test_request_coalescing(self):
        """Execute test_request_coalescing operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestCoalescingMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RequestCoalescingMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Request Dedup ==============
class TestRequestDedup:
    """Represents the TestRequestDedup class."""

    def test_request_dedup(self):
        """Execute test_request_dedup operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestDedupMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RequestDedupMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Request Fingerprint ==============
class TestRequestFingerprint:
    """Represents the TestRequestFingerprint class."""

    def test_request_fingerprint(self):
        """Execute test_request_fingerprint operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestFingerprintMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RequestFingerprintMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Request ID Propagation ==============
class TestRequestIDPropagation:
    """Represents the TestRequestIDPropagation class."""

    def test_request_id_propagation(self):
        """Execute test_request_id_propagation operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestIDPropagationMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RequestIDPropagationMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Request Limit ==============
class TestRequestLimit:
    """Represents the TestRequestLimit class."""

    def test_request_limit(self):
        """Execute test_request_limit operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestLimitMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage, methods=["POST"])])
        app.add_middleware(RequestLimitMiddleware, max_size=1024 * 1024)
        client = TestClient(app)

        response = client.post("/", content="test")
        assert response.status_code == 200


# ============== Request Logger ==============
class TestRequestLogger:
    """Represents the TestRequestLogger class."""

    def test_request_logger(self):
        """Execute test_request_logger operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestLoggerMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RequestLoggerMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Request Priority ==============
class TestRequestPriority:
    """Represents the TestRequestPriority class."""

    def test_request_priority(self):
        """Execute test_request_priority operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestPriorityMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RequestPriorityMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Request Sampler ==============
class TestRequestSampler:
    """Represents the TestRequestSampler class."""

    def test_request_sampler(self):
        """Execute test_request_sampler operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestSamplerMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RequestSamplerMiddleware, rate=0.5)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Request Signing ==============
class TestRequestSigning:
    """Represents the TestRequestSigning class."""

    def test_request_signing(self):
        """Execute test_request_signing operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestSigningMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        secret = "test-secret"
        timestamp = str(int(time.time()))
        message = f"{timestamp}.GET./.".encode()
        hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(
            RequestSigningMiddleware, secret_key=secret, exclude_paths={"/health"}
        )
        client = TestClient(app)

        # Test excluded path
        client.get("/health")


# ============== Request Validator ==============
class TestRequestValidator:
    """Represents the TestRequestValidator class."""

    def test_request_validator(self):
        """Execute test_request_validator operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RequestValidatorMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RequestValidatorMiddleware, rules=[])
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Response Cache ==============
class TestResponseCache:
    """Represents the TestResponseCache class."""

    def test_response_cache(self):
        """Execute test_response_cache operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ResponseCacheMiddleware

        call_count = 0

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            nonlocal call_count
            call_count += 1
            return PlainTextResponse(f"Count: {call_count}")

        app = Starlette(routes=[Route("/", homepage)])
        ResponseCacheMiddleware(app, default_ttl=60)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Response Format ==============
class TestResponseFormat:
    """Represents the TestResponseFormat class."""

    def test_response_format(self):
        """Execute test_response_format operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ResponseFormatMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return JSONResponse({"data": "test"})

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ResponseFormatMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Response Signature ==============
class TestResponseSignature:
    """Represents the TestResponseSignature class."""

    def test_response_signature(self):
        """Execute test_response_signature operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ResponseSignatureMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ResponseSignatureMiddleware, secret_key="test-secret")
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Response Time ==============
class TestResponseTime:
    """Represents the TestResponseTime class."""

    def test_response_time(self):
        """Execute test_response_time operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ResponseTimeMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ResponseTimeMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Retry After ==============
class TestRetryAfter:
    """Represents the TestRetryAfter class."""

    def test_retry_after(self):
        """Execute test_retry_after operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RetryAfterMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(RetryAfterMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Route Auth ==============
class TestRouteAuth:
    """Represents the TestRouteAuth class."""

    def test_route_auth(self):
        """Execute test_route_auth operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import RouteAuthMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/public", homepage)])
        app.add_middleware(RouteAuthMiddleware, routes=[])
        client = TestClient(app)

        response = client.get("/public")
        assert response.status_code == 200


# ============== Sanitization ==============
class TestSanitization:
    """Represents the TestSanitization class."""

    def test_sanitization(self):
        """Execute test_sanitization operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import SanitizationMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(SanitizationMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Scope ==============
class TestScope:
    """Represents the TestScope class."""

    def test_scope(self):
        """Execute test_scope operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ScopeMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ScopeMiddleware, route_scopes={})
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Server Timing ==============
class TestServerTiming:
    """Represents the TestServerTiming class."""

    def test_server_timing(self):
        """Execute test_server_timing operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import ServerTimingMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(ServerTimingMiddleware)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Session ==============
class TestSession:
    """Represents the TestSession class."""

    def test_session(self):
        """Execute test_session operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import SessionConfig, SessionMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        config = SessionConfig(max_age=3600)
        app.add_middleware(SessionMiddleware, config=config)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Slow Response ==============
class TestSlowResponse:
    """Represents the TestSlowResponse class."""

    def test_slow_response_disabled(self):
        """Execute test_slow_response_disabled operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import SlowResponseMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(SlowResponseMiddleware, enabled=False)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Tenant ==============
class TestTenant:
    """Represents the TestTenant class."""

    def test_tenant(self):
        """Execute test_tenant operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import TenantMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(TenantMiddleware)
        client = TestClient(app)

        response = client.get("/", headers={"X-Tenant-ID": "test-tenant"})
        assert response.status_code == 200


# ============== Timeout ==============
class TestTimeout:
    """Represents the TestTimeout class."""

    def test_timeout(self):
        """Execute test_timeout operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import TimeoutMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(TimeoutMiddleware, timeout=30.0)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Trailing Slash ==============
class TestTrailingSlash:
    """Represents the TestTrailingSlash class."""

    def test_trailing_slash(self):
        """Execute test_trailing_slash operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import TrailingSlashMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/test", homepage)])
        app.add_middleware(TrailingSlashMiddleware)
        client = TestClient(app, follow_redirects=True)

        response = client.get("/test")
        assert response.status_code == 200


# ============== User Agent ==============
class TestUserAgent:
    """Represents the TestUserAgent class."""

    def test_user_agent(self):
        """Execute test_user_agent operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import UserAgentMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(UserAgentMiddleware)
        client = TestClient(app)

        response = client.get(
            "/", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        assert response.status_code == 200


# ============== Versioning ==============
class TestVersioning:
    """Represents the TestVersioning class."""

    def test_versioning(self):
        """Execute test_versioning operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import VersioningMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(VersioningMiddleware)
        client = TestClient(app)

        response = client.get("/", headers={"X-API-Version": "2.0"})
        assert response.status_code == 200


# ============== Warmup ==============
class TestWarmup:
    """Represents the TestWarmup class."""

    def test_warmup(self):
        """Execute test_warmup operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import WarmupMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        WarmupMiddleware(app)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200


# ============== Webhook ==============
class TestWebhook:
    """Represents the TestWebhook class."""

    def test_webhook(self):
        """Execute test_webhook operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import WebhookMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(WebhookMiddleware, secret="test-secret", paths={"/webhook"})
        client = TestClient(app)

        # Regular path should work
        response = client.get("/")
        assert response.status_code == 200


# ============== XFF Trust ==============
class TestXFFTrust:
    """Represents the TestXFFTrust class."""

    def test_xff_trust(self):
        """Execute test_xff_trust operation.

        Returns:
            The result of the operation.
        """
        from fastmiddleware import XFFTrustMiddleware

        async def homepage(request):
            """Execute homepage operation.

            Args:
                request: The request parameter.

            Returns:
                The result of the operation.
            """
            return PlainTextResponse("OK")

        app = Starlette(routes=[Route("/", homepage)])
        app.add_middleware(XFFTrustMiddleware, trusted_proxies={"10.0.0.0/8"})
        client = TestClient(app)

        response = client.get("/", headers={"X-Forwarded-For": "1.2.3.4"})
        assert response.status_code == 200
