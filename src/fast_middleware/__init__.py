"""FastMVC Middleware - Production-ready middlewares for FastAPI applications.

A comprehensive collection of 90+ battle-tested, configurable middleware components
for building robust FastAPI/Starlette applications.
"""

from fastmiddleware.mw_core.base import FastMVCMiddleware

# ============================================================================
# Factory & Utilities
# ============================================================================
from fastmiddleware.mw_core.factory import (
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
from fastmiddleware.mw_core.cors import CORSMiddleware
from fastmiddleware.mw_core.cors_preset import CORSPreset
from fastmiddleware.mw_core.logging import LoggingMiddleware
from fastmiddleware.mw_core.timing import (
    DEFAULT_RESPONSE_TIME_HEADER,
    ResponseTimingMiddleware,
)
from fastmiddleware.mw_core.body_limit import BodySizeLimitMiddleware
from fastmiddleware.mw_core.client_ip import (
    STATE_CLIENT_IP,
    ClientIPMiddleware,
    get_client_ip,
    read_client_ip,
)
from fastmiddleware.mw_core.request_id import RequestIDMiddleware

# ============================================================================
# Security Middlewares
# ============================================================================
from fastmiddleware.sec.security import SecurityHeadersMiddleware, SecurityHeadersConfig
from fastmiddleware.sec.trusted_host import TrustedHostMiddleware
from fastmiddleware.sec.csrf import CSRFMiddleware, CSRFConfig
from fastmiddleware.sec.https_redirect import (
    HTTPSRedirectMiddleware,
    HTTPSRedirectConfig,
)
from fastmiddleware.sec.ip_filter import IPFilterMiddleware, IPFilterConfig
from fastmiddleware.sec.origin import OriginMiddleware, OriginConfig
from fastmiddleware.sec.webhook import WebhookMiddleware, WebhookConfig
from fastmiddleware.sec.referrer_policy import (
    ReferrerPolicyMiddleware,
    ReferrerPolicyConfig,
)
from fastmiddleware.sec.permissions_policy import (
    PermissionsPolicyMiddleware,
    PermissionsPolicyConfig,
)
from fastmiddleware.sec.csp_report import CSPReportMiddleware, CSPReportConfig
from fastmiddleware.sec.replay_prevention import (
    ReplayPreventionMiddleware,
    ReplayPreventionConfig,
)
from fastmiddleware.sec.request_signing import (
    RequestSigningMiddleware,
    RequestSigningConfig,
)
from fastmiddleware.sec.honeypot import HoneypotMiddleware, HoneypotConfig
from fastmiddleware.sec.sanitization import SanitizationMiddleware, SanitizationConfig

# ============================================================================
# Rate Limiting & Protection
# ============================================================================
from fastmiddleware.operations.rate_limit import (
    RateLimitMiddleware,
    RateLimitConfig,
    RateLimitStore,
    InMemoryRateLimitStore,
)
from fastmiddleware.operations.quota import QuotaMiddleware, QuotaConfig
from fastmiddleware.operations.load_shedding import (
    LoadSheddingMiddleware,
    LoadSheddingConfig,
)
from fastmiddleware.operations.bulkhead import BulkheadMiddleware, BulkheadConfig
from fastmiddleware.operations.request_dedup import (
    RequestDedupMiddleware,
    RequestDedupConfig,
)
from fastmiddleware.operations.request_coalescing import (
    RequestCoalescingMiddleware,
    CoalescingConfig,
)

# ============================================================================
# Authentication & Authorization
# ============================================================================
from fastmiddleware.sec.authentication import (
    AuthenticationMiddleware,
    AuthConfig,
    AuthBackend,
    JWTAuthBackend,
    APIKeyAuthBackend,
)
from fastmiddleware.sec.basic_auth import BasicAuthMiddleware, BasicAuthConfig
from fastmiddleware.sec.bearer_auth import BearerAuthMiddleware, BearerAuthConfig
from fastmiddleware.sec.scope import ScopeMiddleware, ScopeConfig
from fastmiddleware.sec.route_auth import (
    RouteAuthMiddleware,
    RouteAuthConfig,
    RouteAuth,
)

# ============================================================================
# Session & Context
# ============================================================================
from fastmiddleware.operations.session import (
    SessionMiddleware,
    SessionConfig,
    SessionStore,
    InMemorySessionStore,
    Session,
)
from fastmiddleware.operations.request_context import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)
from fastmiddleware.operations.correlation import (
    CorrelationMiddleware,
    CorrelationConfig,
    get_correlation_id,
)
from fastmiddleware.operations.tenant import (
    TenantMiddleware,
    TenantConfig,
    get_tenant,
    get_tenant_id,
)
from fastmiddleware.operations.context import (
    ContextMiddleware,
    ContextConfig,
    get_context,
    get_context_value,
    set_context_value,
)
from fastmiddleware.operations.request_id_propagation import (
    RequestIDPropagationMiddleware,
    RequestIDPropagationConfig,
    get_request_ids,
    get_trace_header,
)

# ============================================================================
# Response Handling
# ============================================================================
from fastmiddleware.mw_core.compression import CompressionPreset
from fastmiddleware.operations.response_format import (
    ResponseFormatMiddleware,
    ResponseFormatConfig,
)
from fastmiddleware.operations.cache import CacheMiddleware, CacheConfig
from fastmiddleware.operations.etag import ETagMiddleware, ETagConfig
from fastmiddleware.operations.data_masking import (
    DataMaskingMiddleware,
    DataMaskingConfig,
    MaskingRule,
)
from fastmiddleware.operations.response_cache import (
    ResponseCacheMiddleware,
    ResponseCacheConfig,
)
from fastmiddleware.operations.response_signature import (
    ResponseSignatureMiddleware,
    ResponseSignatureConfig,
)
from fastmiddleware.operations.hateoas import HATEOASMiddleware, HATEOASConfig, Link
from fastmiddleware.operations.bandwidth import BandwidthMiddleware, BandwidthConfig
from fastmiddleware.operations.no_cache import NoCacheMiddleware, NoCacheConfig
from fastmiddleware.operations.conditional_request import (
    ConditionalRequestMiddleware,
    ConditionalRequestConfig,
)
from fastmiddleware.operations.early_hints import (
    EarlyHintsMiddleware,
    EarlyHintsConfig,
    EarlyHint,
)

# ============================================================================
# Error Handling
# ============================================================================
from fastmiddleware.operations.error_handler import ErrorHandlerMiddleware, ErrorConfig
from fastmiddleware.operations.circuit_breaker import (
    CircuitBreakerMiddleware,
    CircuitBreakerConfig,
    CircuitState,
)
from fastmiddleware.operations.exception_handler import (
    ExceptionHandlerMiddleware,
    ExceptionHandlerConfig,
)

# ============================================================================
# Health & Monitoring
# ============================================================================
from fastmiddleware.operations.health import HealthCheckMiddleware, HealthConfig
from fastmiddleware.operations.metrics import (
    MetricsMiddleware,
    MetricsConfig,
    MetricsCollector,
)
from fastmiddleware.operations.profiling import ProfilingMiddleware, ProfilingConfig
from fastmiddleware.operations.audit import AuditMiddleware, AuditConfig, AuditEvent
from fastmiddleware.operations.response_time import (
    ResponseTimeMiddleware,
    ResponseTimeConfig,
    ResponseTimeSLA,
)
from fastmiddleware.operations.server_timing import (
    ServerTimingMiddleware,
    ServerTimingConfig,
    timing,
    add_timing,
)
from fastmiddleware.operations.request_logger import (
    RequestLoggerMiddleware,
    RequestLoggerConfig,
)
from fastmiddleware.operations.cost_tracking import (
    CostTrackingMiddleware,
    CostTrackingConfig,
    get_request_cost,
    add_cost,
)
from fastmiddleware.operations.request_sampler import (
    RequestSamplerMiddleware,
    RequestSamplerConfig,
    is_sampled,
)

# ============================================================================
# Idempotency
# ============================================================================
from fastmiddleware.operations.idempotency import (
    IdempotencyMiddleware,
    IdempotencyConfig,
    IdempotencyStore,
    InMemoryIdempotencyStore,
)

# ============================================================================
# Maintenance & Lifecycle
# ============================================================================
from fastmiddleware.operations.maintenance import (
    MaintenanceMiddleware,
    MaintenanceConfig,
)
from fastmiddleware.operations.warmup import WarmupMiddleware, WarmupConfig
from fastmiddleware.operations.graceful_shutdown import (
    GracefulShutdownMiddleware,
    GracefulShutdownConfig,
)
from fastmiddleware.operations.chaos import ChaosMiddleware, ChaosConfig
from fastmiddleware.operations.slow_response import (
    SlowResponseMiddleware,
    SlowResponseConfig,
)

# ============================================================================
# Request Processing
# ============================================================================
from fastmiddleware.operations.timeout import TimeoutMiddleware, TimeoutConfig
from fastmiddleware.operations.request_limit import (
    RequestLimitMiddleware,
    RequestLimitConfig,
)
from fastmiddleware.operations.trailing_slash import (
    TrailingSlashMiddleware,
    TrailingSlashConfig,
    SlashAction,
)
from fastmiddleware.operations.content_type import (
    ContentTypeMiddleware,
    ContentTypeConfig,
)
from fastmiddleware.operations.header_transform import (
    HeaderTransformMiddleware,
    HeaderTransformConfig,
)
from fastmiddleware.operations.request_validator import (
    RequestValidatorMiddleware,
    RequestValidatorConfig,
    ValidationRule,
)
from fastmiddleware.operations.json_schema import JSONSchemaMiddleware, JSONSchemaConfig
from fastmiddleware.operations.payload_size import (
    PayloadSizeMiddleware,
    PayloadSizeConfig,
)
from fastmiddleware.operations.method_override import (
    MethodOverrideMiddleware,
    MethodOverrideConfig,
)
from fastmiddleware.operations.request_fingerprint import (
    RequestFingerprintMiddleware,
    FingerprintConfig,
    get_fingerprint,
)
from fastmiddleware.operations.request_priority import (
    RequestPriorityMiddleware,
    PriorityConfig,
    Priority,
)

# ============================================================================
# URL & Routing
# ============================================================================
from fastmiddleware.operations.redirect import (
    RedirectMiddleware,
    RedirectConfig,
    RedirectRule,
)
from fastmiddleware.operations.path_rewrite import (
    PathRewriteMiddleware,
    PathRewriteConfig,
    RewriteRule,
)
from fastmiddleware.operations.proxy import ProxyMiddleware, ProxyConfig, ProxyRoute

# ============================================================================
# API Management
# ============================================================================
from fastmiddleware.operations.versioning import (
    VersioningMiddleware,
    VersioningConfig,
    VersionLocation,
    get_api_version,
)
from fastmiddleware.operations.deprecation import (
    DeprecationMiddleware,
    DeprecationConfig,
    DeprecationInfo,
)
from fastmiddleware.operations.retry_after import RetryAfterMiddleware, RetryAfterConfig
from fastmiddleware.operations.api_version_header import (
    APIVersionHeaderMiddleware,
    APIVersionHeaderConfig,
)

# ============================================================================
# Detection & Analytics
# ============================================================================
from fastmiddleware.operations.bot_detection import (
    BotDetectionMiddleware,
    BotConfig,
    BotAction,
)
from fastmiddleware.operations.geoip import GeoIPMiddleware, GeoIPConfig, get_geo_data
from fastmiddleware.operations.user_agent import (
    UserAgentMiddleware,
    UserAgentConfig,
    UserAgentInfo,
    get_user_agent,
)

# ============================================================================
# Feature Management & Testing
# ============================================================================
from fastmiddleware.operations.feature_flag import (
    FeatureFlagMiddleware,
    FeatureFlagConfig,
    get_feature_flags,
    is_feature_enabled,
)
from fastmiddleware.operations.ab_testing import (
    ABTestMiddleware,
    ABTestConfig,
    Experiment,
    get_variant,
)

# ============================================================================
# Localization & Content Negotiation
# ============================================================================
from fastmiddleware.operations.locale import LocaleMiddleware, LocaleConfig, get_locale
from fastmiddleware.operations.accept_language import (
    AcceptLanguageMiddleware,
    AcceptLanguageConfig,
    get_language,
)
from fastmiddleware.operations.content_negotiation import (
    ContentNegotiationMiddleware,
    ContentNegotiationConfig,
    get_negotiated_type,
)
from fastmiddleware.operations.client_hints import (
    ClientHintsMiddleware,
    ClientHintsConfig,
    get_client_hints,
)

# ============================================================================
# IP & Proxy Handling
# ============================================================================
from fastmiddleware.operations.real_ip import (
    RealIPMiddleware,
    RealIPConfig,
    get_real_ip,
)
from fastmiddleware.operations.xff_trust import XFFTrustMiddleware, XFFTrustConfig

# ============================================================================
# Observability, privacy & static asset caching
# ============================================================================
from fastmiddleware.operations.build_version import (
    BuildVersionMiddleware,
    BuildVersionConfig,
)
from fastmiddleware.operations.immutable_static_cache import (
    ImmutableStaticCacheMiddleware,
    ImmutableStaticCacheConfig,
)
from fastmiddleware.operations.edge_performance_tiers import (
    EdgePerformanceTier,
    EdgeTierCacheHeadersConfig,
    EdgeTierCacheHeadersMiddleware,
    EdgeTierDefinition,
    tier_definition,
)
from fastmiddleware.operations.dns_prefetch_control import (
    DNSPrefetchControlMiddleware,
    DNSPrefetchControlConfig,
)

__version__ = "0.6.4"
__author__ = "Shivansh Sengar, Shreyansh Sengar"
__email__ = "sengarsinghshivansh@gmail.com, sengarsinghshreyansh@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/shregar1/fast-middleware"

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
