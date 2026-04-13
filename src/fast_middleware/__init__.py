"""FastMVC Middleware - Production-ready middlewares for FastAPI applications.

A comprehensive collection of 90+ battle-tested, configurable middleware components
for building robust FastAPI/Starlette applications.
"""

from fast_middleware.mw_core.base import FastMVCMiddleware

# ============================================================================
# Factory & Utilities
# ============================================================================
from fast_middleware.mw_core.factory import (
    create_middleware,
    middleware,
    MiddlewareBuilder,
    MiddlewareConfig,
    add_middleware_once,
    quick_middleware,
    is_middleware_registered,
    clear_registry,
)

# ============================================================================
# Core Middlewares
# ============================================================================
from fast_middleware.mw_core.cors import CORSMiddleware
from fast_middleware.mw_core.cors_preset import CORSPreset
from fast_middleware.mw_core.logging import LoggingMiddleware
from fast_middleware.mw_core.timing import (
    DEFAULT_RESPONSE_TIME_HEADER,
    ResponseTimingMiddleware,
)
from fast_middleware.mw_core.body_limit import BodySizeLimitMiddleware
from fast_middleware.mw_core.client_ip import (
    STATE_CLIENT_IP,
    ClientIPMiddleware,
    get_client_ip,
    read_client_ip,
)
from fast_middleware.mw_core.request_id import RequestIDMiddleware

# ============================================================================
# Security Middlewares
# ============================================================================
from fast_middleware.sec.security import SecurityHeadersMiddleware, SecurityHeadersConfig
from fast_middleware.sec.trusted_host import TrustedHostMiddleware
from fast_middleware.sec.csrf import CSRFMiddleware, CSRFConfig
from fast_middleware.sec.https_redirect import (
    HTTPSRedirectMiddleware,
    HTTPSRedirectConfig,
)
from fast_middleware.sec.ip_filter import IPFilterMiddleware, IPFilterConfig
from fast_middleware.sec.origin import OriginMiddleware, OriginConfig
from fast_middleware.sec.webhook import WebhookMiddleware, WebhookConfig
from fast_middleware.sec.referrer_policy import (
    ReferrerPolicyMiddleware,
    ReferrerPolicyConfig,
)
from fast_middleware.sec.permissions_policy import (
    PermissionsPolicyMiddleware,
    PermissionsPolicyConfig,
)
from fast_middleware.sec.csp_report import CSPReportMiddleware, CSPReportConfig
from fast_middleware.sec.replay_prevention import (
    ReplayPreventionMiddleware,
    ReplayPreventionConfig,
)
from fast_middleware.sec.request_signing import (
    RequestSigningMiddleware,
    RequestSigningConfig,
)
from fast_middleware.sec.honeypot import HoneypotMiddleware, HoneypotConfig
from fast_middleware.sec.sanitization import SanitizationMiddleware, SanitizationConfig

# ============================================================================
# Rate Limiting & Protection
# ============================================================================
from fast_middleware.operations.rate_limit import (
    RateLimitMiddleware,
    RateLimitConfig,
    RateLimitStore,
    InMemoryRateLimitStore,
)
from fast_middleware.operations.quota import QuotaMiddleware, QuotaConfig
from fast_middleware.operations.load_shedding import (
    LoadSheddingMiddleware,
    LoadSheddingConfig,
)
from fast_middleware.operations.bulkhead import BulkheadMiddleware, BulkheadConfig
from fast_middleware.operations.request_dedup import (
    RequestDedupMiddleware,
    RequestDedupConfig,
)
from fast_middleware.operations.request_coalescing import (
    RequestCoalescingMiddleware,
    CoalescingConfig,
)

# ============================================================================
# Authentication & Authorization
# ============================================================================
from fast_middleware.sec.authentication import (
    AuthenticationMiddleware,
    AuthConfig,
    AuthBackend,
    JWTAuthBackend,
    APIKeyAuthBackend,
)
from fast_middleware.sec.basic_auth import BasicAuthMiddleware, BasicAuthConfig
from fast_middleware.sec.bearer_auth import BearerAuthMiddleware, BearerAuthConfig
from fast_middleware.sec.scope import ScopeMiddleware, ScopeConfig
from fast_middleware.sec.route_auth import (
    RouteAuthMiddleware,
    RouteAuthConfig,
    RouteAuth,
)

# ============================================================================
# Session & Context
# ============================================================================
from fast_middleware.operations.session import (
    SessionMiddleware,
    SessionConfig,
    SessionStore,
    InMemorySessionStore,
    Session,
)
from fast_middleware.operations.request_context import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)
from fast_middleware.operations.correlation import (
    CorrelationMiddleware,
    CorrelationConfig,
    get_correlation_id,
)
from fast_middleware.operations.tenant import (
    TenantMiddleware,
    TenantConfig,
    get_tenant,
    get_tenant_id,
)
from fast_middleware.operations.context import (
    ContextMiddleware,
    ContextConfig,
    get_context,
    get_context_value,
    set_context_value,
)
from fast_middleware.operations.request_id_propagation import (
    RequestIDPropagationMiddleware,
    RequestIDPropagationConfig,
    get_request_ids,
    get_trace_header,
)

# ============================================================================
# Response Handling
# ============================================================================
from fast_middleware.mw_core.compression import CompressionPreset
from fast_middleware.operations.response_format import (
    ResponseFormatMiddleware,
    ResponseFormatConfig,
)
from fast_middleware.operations.cache import CacheMiddleware, CacheConfig
from fast_middleware.operations.etag import ETagMiddleware, ETagConfig
from fast_middleware.operations.data_masking import (
    DataMaskingMiddleware,
    DataMaskingConfig,
    MaskingRule,
)
from fast_middleware.operations.response_cache import (
    ResponseCacheMiddleware,
    ResponseCacheConfig,
)
from fast_middleware.operations.response_signature import (
    ResponseSignatureMiddleware,
    ResponseSignatureConfig,
)
from fast_middleware.operations.hateoas import HATEOASMiddleware, HATEOASConfig, Link
from fast_middleware.operations.bandwidth import BandwidthMiddleware, BandwidthConfig
from fast_middleware.operations.no_cache import NoCacheMiddleware, NoCacheConfig
from fast_middleware.operations.conditional_request import (
    ConditionalRequestMiddleware,
    ConditionalRequestConfig,
)
from fast_middleware.operations.early_hints import (
    EarlyHintsMiddleware,
    EarlyHintsConfig,
    EarlyHint,
)

# ============================================================================
# Error Handling
# ============================================================================
from fast_middleware.operations.error_handler import ErrorHandlerMiddleware, ErrorConfig
from fast_middleware.operations.circuit_breaker import (
    CircuitBreakerMiddleware,
    CircuitBreakerConfig,
    CircuitState,
)
from fast_middleware.operations.exception_handler import (
    ExceptionHandlerMiddleware,
    ExceptionHandlerConfig,
)

# ============================================================================
# Health & Monitoring
# ============================================================================
from fast_middleware.operations.health import HealthCheckMiddleware, HealthConfig
from fast_middleware.operations.metrics import (
    MetricsMiddleware,
    MetricsConfig,
    MetricsCollector,
)
from fast_middleware.operations.profiling import ProfilingMiddleware, ProfilingConfig
from fast_middleware.operations.audit import AuditMiddleware, AuditConfig, AuditEvent
from fast_middleware.operations.response_time import (
    ResponseTimeMiddleware,
    ResponseTimeConfig,
    ResponseTimeSLA,
)
from fast_middleware.operations.server_timing import (
    ServerTimingMiddleware,
    ServerTimingConfig,
    timing,
    add_timing,
)
from fast_middleware.operations.request_logger import (
    RequestLoggerMiddleware,
    RequestLoggerConfig,
)
from fast_middleware.operations.cost_tracking import (
    CostTrackingMiddleware,
    CostTrackingConfig,
    get_request_cost,
    add_cost,
)
from fast_middleware.operations.request_sampler import (
    RequestSamplerMiddleware,
    RequestSamplerConfig,
    is_sampled,
)

# ============================================================================
# Idempotency
# ============================================================================
from fast_middleware.operations.idempotency import (
    IdempotencyMiddleware,
    IdempotencyConfig,
    IdempotencyStore,
    InMemoryIdempotencyStore,
)

# ============================================================================
# Maintenance & Lifecycle
# ============================================================================
from fast_middleware.operations.maintenance import (
    MaintenanceMiddleware,
    MaintenanceConfig,
)
from fast_middleware.operations.warmup import WarmupMiddleware, WarmupConfig
from fast_middleware.operations.graceful_shutdown import (
    GracefulShutdownMiddleware,
    GracefulShutdownConfig,
)
from fast_middleware.operations.chaos import ChaosMiddleware, ChaosConfig
from fast_middleware.operations.slow_response import (
    SlowResponseMiddleware,
    SlowResponseConfig,
)

# ============================================================================
# Request Processing
# ============================================================================
from fast_middleware.operations.timeout import TimeoutMiddleware, TimeoutConfig
from fast_middleware.operations.request_limit import (
    RequestLimitMiddleware,
    RequestLimitConfig,
)
from fast_middleware.operations.trailing_slash import (
    TrailingSlashMiddleware,
    TrailingSlashConfig,
    SlashAction,
)
from fast_middleware.operations.content_type import (
    ContentTypeMiddleware,
    ContentTypeConfig,
)
from fast_middleware.operations.header_transform import (
    HeaderTransformMiddleware,
    HeaderTransformConfig,
)
from fast_middleware.operations.request_validator import (
    RequestValidatorMiddleware,
    RequestValidatorConfig,
    ValidationRule,
)
from fast_middleware.operations.json_schema import JSONSchemaMiddleware, JSONSchemaConfig
from fast_middleware.operations.payload_size import (
    PayloadSizeMiddleware,
    PayloadSizeConfig,
)
from fast_middleware.operations.method_override import (
    MethodOverrideMiddleware,
    MethodOverrideConfig,
)
from fast_middleware.operations.request_fingerprint import (
    RequestFingerprintMiddleware,
    FingerprintConfig,
    get_fingerprint,
)
from fast_middleware.operations.request_priority import (
    RequestPriorityMiddleware,
    PriorityConfig,
    Priority,
)

# ============================================================================
# URL & Routing
# ============================================================================
from fast_middleware.operations.redirect import (
    RedirectMiddleware,
    RedirectConfig,
    RedirectRule,
)
from fast_middleware.operations.path_rewrite import (
    PathRewriteMiddleware,
    PathRewriteConfig,
    RewriteRule,
)
from fast_middleware.operations.proxy import ProxyMiddleware, ProxyConfig, ProxyRoute

# ============================================================================
# API Management
# ============================================================================
from fast_middleware.operations.versioning import (
    VersioningMiddleware,
    VersioningConfig,
    VersionLocation,
    get_api_version,
)
from fast_middleware.operations.deprecation import (
    DeprecationMiddleware,
    DeprecationConfig,
    DeprecationInfo,
)
from fast_middleware.operations.retry_after import RetryAfterMiddleware, RetryAfterConfig
from fast_middleware.operations.api_version_header import (
    APIVersionHeaderMiddleware,
    APIVersionHeaderConfig,
)

# ============================================================================
# Detection & Analytics
# ============================================================================
from fast_middleware.operations.bot_detection import (
    BotDetectionMiddleware,
    BotConfig,
    BotAction,
)
from fast_middleware.operations.geoip import GeoIPMiddleware, GeoIPConfig, get_geo_data
from fast_middleware.operations.user_agent import (
    UserAgentMiddleware,
    UserAgentConfig,
    UserAgentInfo,
    get_user_agent,
)

# ============================================================================
# Feature Management & Testing
# ============================================================================
from fast_middleware.operations.feature_flag import (
    FeatureFlagMiddleware,
    FeatureFlagConfig,
    get_feature_flags,
    is_feature_enabled,
)
from fast_middleware.operations.ab_testing import (
    ABTestMiddleware,
    ABTestConfig,
    Experiment,
    get_variant,
)

# ============================================================================
# Localization & Content Negotiation
# ============================================================================
from fast_middleware.operations.locale import LocaleMiddleware, LocaleConfig, get_locale
from fast_middleware.operations.accept_language import (
    AcceptLanguageMiddleware,
    AcceptLanguageConfig,
    get_language,
)
from fast_middleware.operations.content_negotiation import (
    ContentNegotiationMiddleware,
    ContentNegotiationConfig,
    get_negotiated_type,
)
from fast_middleware.operations.client_hints import (
    ClientHintsMiddleware,
    ClientHintsConfig,
    get_client_hints,
)

# ============================================================================
# IP & Proxy Handling
# ============================================================================
from fast_middleware.operations.real_ip import (
    RealIPMiddleware,
    RealIPConfig,
    get_real_ip,
)
from fast_middleware.operations.xff_trust import XFFTrustMiddleware, XFFTrustConfig

# ============================================================================
# Observability, privacy & static asset caching
# ============================================================================
from fast_middleware.operations.build_version import (
    BuildVersionMiddleware,
    BuildVersionConfig,
)
from fast_middleware.operations.immutable_static_cache import (
    ImmutableStaticCacheMiddleware,
    ImmutableStaticCacheConfig,
)
from fast_middleware.operations.edge_performance_tiers import (
    EdgePerformanceTier,
    EdgeTierCacheHeadersConfig,
    EdgeTierCacheHeadersMiddleware,
    EdgeTierDefinition,
    tier_definition,
)
from fast_middleware.operations.dns_prefetch_control import (
    DNSPrefetchControlMiddleware,
    DNSPrefetchControlConfig,
)

__version__ = "1.6.0"
__author__ = "Shivansh Sengar, Shreyansh Sengar"
__email__ = "sengarsinghshivansh@gmail.com, sengarsinghshreyansh@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/shregar1/fastMVC"

__all__ = [
    # Base
    "FastMVCMiddleware",
    # Core
    "CORSMiddleware",
    "CORSPreset",
    "LoggingMiddleware",
    "DEFAULT_RESPONSE_TIME_HEADER",
    "ResponseTimingMiddleware",
    "BodySizeLimitMiddleware",
    "STATE_CLIENT_IP",
    "ClientIPMiddleware",
    "get_client_ip",
    "read_client_ip",
    "RequestIDMiddleware",
    # Security
    "SecurityHeadersMiddleware",
    "SecurityHeadersConfig",
    "TrustedHostMiddleware",
    "CSRFMiddleware",
    "CSRFConfig",
    "HTTPSRedirectMiddleware",
    "HTTPSRedirectConfig",
    "IPFilterMiddleware",
    "IPFilterConfig",
    "OriginMiddleware",
    "OriginConfig",
    "WebhookMiddleware",
    "WebhookConfig",
    "ReferrerPolicyMiddleware",
    "ReferrerPolicyConfig",
    "PermissionsPolicyMiddleware",
    "PermissionsPolicyConfig",
    "CSPReportMiddleware",
    "CSPReportConfig",
    "ReplayPreventionMiddleware",
    "ReplayPreventionConfig",
    "RequestSigningMiddleware",
    "RequestSigningConfig",
    "HoneypotMiddleware",
    "HoneypotConfig",
    "SanitizationMiddleware",
    "SanitizationConfig",
    # Rate Limiting & Protection
    "RateLimitMiddleware",
    "RateLimitConfig",
    "RateLimitStore",
    "InMemoryRateLimitStore",
    "QuotaMiddleware",
    "QuotaConfig",
    "LoadSheddingMiddleware",
    "LoadSheddingConfig",
    "BulkheadMiddleware",
    "BulkheadConfig",
    "RequestDedupMiddleware",
    "RequestDedupConfig",
    "RequestCoalescingMiddleware",
    "CoalescingConfig",
    # Authentication
    "AuthenticationMiddleware",
    "AuthConfig",
    "AuthBackend",
    "JWTAuthBackend",
    "APIKeyAuthBackend",
    "BasicAuthMiddleware",
    "BasicAuthConfig",
    "BearerAuthMiddleware",
    "BearerAuthConfig",
    "ScopeMiddleware",
    "ScopeConfig",
    "RouteAuthMiddleware",
    "RouteAuthConfig",
    "RouteAuth",
    # Session & Context
    "SessionMiddleware",
    "SessionConfig",
    "SessionStore",
    "InMemorySessionStore",
    "Session",
    "RequestContextMiddleware",
    "get_request_id",
    "get_request_context",
    "CorrelationMiddleware",
    "CorrelationConfig",
    "get_correlation_id",
    "TenantMiddleware",
    "TenantConfig",
    "get_tenant",
    "get_tenant_id",
    "ContextMiddleware",
    "ContextConfig",
    "get_context",
    "get_context_value",
    "set_context_value",
    "RequestIDPropagationMiddleware",
    "RequestIDPropagationConfig",
    "get_request_ids",
    "get_trace_header",
    # Response Handling
    "CompressionPreset",
    "ResponseFormatMiddleware",
    "ResponseFormatConfig",
    "CacheMiddleware",
    "CacheConfig",
    "ETagMiddleware",
    "ETagConfig",
    "DataMaskingMiddleware",
    "DataMaskingConfig",
    "MaskingRule",
    "ResponseCacheMiddleware",
    "ResponseCacheConfig",
    "ResponseSignatureMiddleware",
    "ResponseSignatureConfig",
    "HATEOASMiddleware",
    "HATEOASConfig",
    "Link",
    "BandwidthMiddleware",
    "BandwidthConfig",
    "NoCacheMiddleware",
    "NoCacheConfig",
    "ConditionalRequestMiddleware",
    "ConditionalRequestConfig",
    "EarlyHintsMiddleware",
    "EarlyHintsConfig",
    "EarlyHint",
    # Error Handling
    "ErrorHandlerMiddleware",
    "ErrorConfig",
    "CircuitBreakerMiddleware",
    "CircuitBreakerConfig",
    "CircuitState",
    "ExceptionHandlerMiddleware",
    "ExceptionHandlerConfig",
    # Health & Monitoring
    "HealthCheckMiddleware",
    "HealthConfig",
    "MetricsMiddleware",
    "MetricsConfig",
    "MetricsCollector",
    "ProfilingMiddleware",
    "ProfilingConfig",
    "AuditMiddleware",
    "AuditConfig",
    "AuditEvent",
    "ResponseTimeMiddleware",
    "ResponseTimeConfig",
    "ResponseTimeSLA",
    "ServerTimingMiddleware",
    "ServerTimingConfig",
    "timing",
    "add_timing",
    "RequestLoggerMiddleware",
    "RequestLoggerConfig",
    "CostTrackingMiddleware",
    "CostTrackingConfig",
    "get_request_cost",
    "add_cost",
    "RequestSamplerMiddleware",
    "RequestSamplerConfig",
    "is_sampled",
    # Idempotency
    "IdempotencyMiddleware",
    "IdempotencyConfig",
    "IdempotencyStore",
    "InMemoryIdempotencyStore",
    # Maintenance & Lifecycle
    "MaintenanceMiddleware",
    "MaintenanceConfig",
    "WarmupMiddleware",
    "WarmupConfig",
    "GracefulShutdownMiddleware",
    "GracefulShutdownConfig",
    "ChaosMiddleware",
    "ChaosConfig",
    "SlowResponseMiddleware",
    "SlowResponseConfig",
    # Request Processing
    "TimeoutMiddleware",
    "TimeoutConfig",
    "RequestLimitMiddleware",
    "RequestLimitConfig",
    "TrailingSlashMiddleware",
    "TrailingSlashConfig",
    "SlashAction",
    "ContentTypeMiddleware",
    "ContentTypeConfig",
    "HeaderTransformMiddleware",
    "HeaderTransformConfig",
    "RequestValidatorMiddleware",
    "RequestValidatorConfig",
    "ValidationRule",
    "JSONSchemaMiddleware",
    "JSONSchemaConfig",
    "PayloadSizeMiddleware",
    "PayloadSizeConfig",
    "MethodOverrideMiddleware",
    "MethodOverrideConfig",
    "RequestFingerprintMiddleware",
    "FingerprintConfig",
    "get_fingerprint",
    "RequestPriorityMiddleware",
    "PriorityConfig",
    "Priority",
    # URL & Routing
    "RedirectMiddleware",
    "RedirectConfig",
    "RedirectRule",
    "PathRewriteMiddleware",
    "PathRewriteConfig",
    "RewriteRule",
    "ProxyMiddleware",
    "ProxyConfig",
    "ProxyRoute",
    # API Management
    "VersioningMiddleware",
    "VersioningConfig",
    "VersionLocation",
    "get_api_version",
    "DeprecationMiddleware",
    "DeprecationConfig",
    "DeprecationInfo",
    "RetryAfterMiddleware",
    "RetryAfterConfig",
    "APIVersionHeaderMiddleware",
    "APIVersionHeaderConfig",
    # Detection & Analytics
    "BotDetectionMiddleware",
    "BotConfig",
    "BotAction",
    "GeoIPMiddleware",
    "GeoIPConfig",
    "get_geo_data",
    "UserAgentMiddleware",
    "UserAgentConfig",
    "UserAgentInfo",
    "get_user_agent",
    # Feature Management & Testing
    "FeatureFlagMiddleware",
    "FeatureFlagConfig",
    "get_feature_flags",
    "is_feature_enabled",
    "ABTestMiddleware",
    "ABTestConfig",
    "Experiment",
    "get_variant",
    # Localization & Content Negotiation
    "LocaleMiddleware",
    "LocaleConfig",
    "get_locale",
    "AcceptLanguageMiddleware",
    "AcceptLanguageConfig",
    "get_language",
    "ContentNegotiationMiddleware",
    "ContentNegotiationConfig",
    "get_negotiated_type",
    "ClientHintsMiddleware",
    "ClientHintsConfig",
    "get_client_hints",
    # IP & Proxy Handling
    "RealIPMiddleware",
    "RealIPConfig",
    "get_real_ip",
    "XFFTrustMiddleware",
    "XFFTrustConfig",
    # Observability, privacy & static asset caching
    "BuildVersionMiddleware",
    "BuildVersionConfig",
    "ImmutableStaticCacheMiddleware",
    "ImmutableStaticCacheConfig",
    "DNSPrefetchControlMiddleware",
    "DNSPrefetchControlConfig",
    # CDN / edge performance tiers
    "EdgePerformanceTier",
    "EdgeTierCacheHeadersConfig",
    "EdgeTierCacheHeadersMiddleware",
    "EdgeTierDefinition",
    "tier_definition",
    # Factory & Utilities
    "create_middleware",
    "middleware",
    "MiddlewareBuilder",
    "MiddlewareConfig",
    "add_middleware_once",
    "quick_middleware",
    "is_middleware_registered",
    "clear_registry",
]
