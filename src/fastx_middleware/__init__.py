"""FastMVC Middleware - Production-ready middlewares for FastAPI applications.

A comprehensive collection of 90+ battle-tested, configurable middleware components
for building robust FastAPI/Starlette applications.
"""

from fastx_middleware.mw_core.base import FastMVCMiddleware

# ============================================================================
# Factory & Utilities
# ============================================================================
from fastx_middleware.mw_core.factory import (
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
from fastx_middleware.mw_core.cors import CORSMiddleware
from fastx_middleware.mw_core.cors_preset import CORSPreset
from fastx_middleware.mw_core.logging import LoggingMiddleware
from fastx_middleware.mw_core.timing import (
    DEFAULT_RESPONSE_TIME_HEADER,
    ResponseTimingMiddleware,
)
from fastx_middleware.mw_core.body_limit import BodySizeLimitMiddleware
from fastx_middleware.mw_core.client_ip import (
    STATE_CLIENT_IP,
    ClientIPMiddleware,
    get_client_ip,
    read_client_ip,
)
from fastx_middleware.mw_core.request_id import RequestIDMiddleware

# ============================================================================
# Security Middlewares
# ============================================================================
from fastx_middleware.sec.security import SecurityHeadersMiddleware, SecurityHeadersConfig
from fastx_middleware.sec.trusted_host import TrustedHostMiddleware
from fastx_middleware.sec.csrf import CSRFMiddleware, CSRFConfig
from fastx_middleware.sec.https_redirect import (
    HTTPSRedirectMiddleware,
    HTTPSRedirectConfig,
)
from fastx_middleware.sec.ip_filter import IPFilterMiddleware, IPFilterConfig
from fastx_middleware.sec.origin import OriginMiddleware, OriginConfig
from fastx_middleware.sec.webhook import WebhookMiddleware, WebhookConfig
from fastx_middleware.sec.referrer_policy import (
    ReferrerPolicyMiddleware,
    ReferrerPolicyConfig,
)
from fastx_middleware.sec.permissions_policy import (
    PermissionsPolicyMiddleware,
    PermissionsPolicyConfig,
)
from fastx_middleware.sec.csp_report import CSPReportMiddleware, CSPReportConfig
from fastx_middleware.sec.replay_prevention import (
    ReplayPreventionMiddleware,
    ReplayPreventionConfig,
)
from fastx_middleware.sec.request_signing import (
    RequestSigningMiddleware,
    RequestSigningConfig,
)
from fastx_middleware.sec.honeypot import HoneypotMiddleware, HoneypotConfig
from fastx_middleware.sec.sanitization import SanitizationMiddleware, SanitizationConfig

# ============================================================================
# Rate Limiting & Protection
# ============================================================================
from fastx_middleware.operations.rate_limit import (
    RateLimitMiddleware,
    RateLimitConfig,
    RateLimitStore,
    InMemoryRateLimitStore,
)
from fastx_middleware.operations.quota import QuotaMiddleware, QuotaConfig
from fastx_middleware.operations.load_shedding import (
    LoadSheddingMiddleware,
    LoadSheddingConfig,
)
from fastx_middleware.operations.bulkhead import BulkheadMiddleware, BulkheadConfig
from fastx_middleware.operations.request_dedup import (
    RequestDedupMiddleware,
    RequestDedupConfig,
)
from fastx_middleware.operations.request_coalescing import (
    RequestCoalescingMiddleware,
    CoalescingConfig,
)

# ============================================================================
# Authentication & Authorization
# ============================================================================
from fastx_middleware.sec.authentication import (
    AuthenticationMiddleware,
    AuthConfig,
    AuthBackend,
    JWTAuthBackend,
    APIKeyAuthBackend,
)
from fastx_middleware.sec.basic_auth import BasicAuthMiddleware, BasicAuthConfig
from fastx_middleware.sec.bearer_auth import BearerAuthMiddleware, BearerAuthConfig
from fastx_middleware.sec.scope import ScopeMiddleware, ScopeConfig
from fastx_middleware.sec.route_auth import (
    RouteAuthMiddleware,
    RouteAuthConfig,
    RouteAuth,
)

# ============================================================================
# Session & Context
# ============================================================================
from fastx_middleware.operations.session import (
    SessionMiddleware,
    SessionConfig,
    SessionStore,
    InMemorySessionStore,
    Session,
)
from fastx_middleware.operations.request_context import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)
from fastx_middleware.operations.correlation import (
    CorrelationMiddleware,
    CorrelationConfig,
    get_correlation_id,
)
from fastx_middleware.operations.tenant import (
    TenantMiddleware,
    TenantConfig,
    get_tenant,
    get_tenant_id,
)
from fastx_middleware.operations.context import (
    ContextMiddleware,
    ContextConfig,
    get_context,
    get_context_value,
    set_context_value,
)
from fastx_middleware.operations.request_id_propagation import (
    RequestIDPropagationMiddleware,
    RequestIDPropagationConfig,
    get_request_ids,
    get_trace_header,
)

# ============================================================================
# Response Handling
# ============================================================================
from fastx_middleware.mw_core.compression import CompressionPreset
from fastx_middleware.operations.response_format import (
    ResponseFormatMiddleware,
    ResponseFormatConfig,
)
from fastx_middleware.operations.cache import CacheMiddleware, CacheConfig
from fastx_middleware.operations.etag import ETagMiddleware, ETagConfig
from fastx_middleware.operations.data_masking import (
    DataMaskingMiddleware,
    DataMaskingConfig,
    MaskingRule,
)
from fastx_middleware.operations.response_cache import (
    ResponseCacheMiddleware,
    ResponseCacheConfig,
)
from fastx_middleware.operations.response_signature import (
    ResponseSignatureMiddleware,
    ResponseSignatureConfig,
)
from fastx_middleware.operations.hateoas import HATEOASMiddleware, HATEOASConfig, Link
from fastx_middleware.operations.bandwidth import BandwidthMiddleware, BandwidthConfig
from fastx_middleware.operations.no_cache import NoCacheMiddleware, NoCacheConfig
from fastx_middleware.operations.conditional_request import (
    ConditionalRequestMiddleware,
    ConditionalRequestConfig,
)
from fastx_middleware.operations.early_hints import (
    EarlyHintsMiddleware,
    EarlyHintsConfig,
    EarlyHint,
)

# ============================================================================
# Error Handling
# ============================================================================
from fastx_middleware.operations.error_handler import ErrorHandlerMiddleware, ErrorConfig
from fastx_middleware.operations.circuit_breaker import (
    CircuitBreakerMiddleware,
    CircuitBreakerConfig,
    CircuitState,
)
from fastx_middleware.operations.exception_handler import (
    ExceptionHandlerMiddleware,
    ExceptionHandlerConfig,
)

# ============================================================================
# Health & Monitoring
# ============================================================================
from fastx_middleware.operations.health import HealthCheckMiddleware, HealthConfig
from fastx_middleware.operations.metrics import (
    MetricsMiddleware,
    MetricsConfig,
    MetricsCollector,
)
from fastx_middleware.operations.profiling import ProfilingMiddleware, ProfilingConfig
from fastx_middleware.operations.audit import AuditMiddleware, AuditConfig, AuditEvent
from fastx_middleware.operations.response_time import (
    ResponseTimeMiddleware,
    ResponseTimeConfig,
    ResponseTimeSLA,
)
from fastx_middleware.operations.server_timing import (
    ServerTimingMiddleware,
    ServerTimingConfig,
    timing,
    add_timing,
)
from fastx_middleware.operations.request_logger import (
    RequestLoggerMiddleware,
    RequestLoggerConfig,
)
from fastx_middleware.operations.cost_tracking import (
    CostTrackingMiddleware,
    CostTrackingConfig,
    get_request_cost,
    add_cost,
)
from fastx_middleware.operations.request_sampler import (
    RequestSamplerMiddleware,
    RequestSamplerConfig,
    is_sampled,
)

# ============================================================================
# Idempotency
# ============================================================================
from fastx_middleware.operations.idempotency import (
    IdempotencyMiddleware,
    IdempotencyConfig,
    IdempotencyStore,
    InMemoryIdempotencyStore,
)

# ============================================================================
# Maintenance & Lifecycle
# ============================================================================
from fastx_middleware.operations.maintenance import (
    MaintenanceMiddleware,
    MaintenanceConfig,
)
from fastx_middleware.operations.warmup import WarmupMiddleware, WarmupConfig
from fastx_middleware.operations.graceful_shutdown import (
    GracefulShutdownMiddleware,
    GracefulShutdownConfig,
)
from fastx_middleware.operations.chaos import ChaosMiddleware, ChaosConfig
from fastx_middleware.operations.slow_response import (
    SlowResponseMiddleware,
    SlowResponseConfig,
)

# ============================================================================
# Request Processing
# ============================================================================
from fastx_middleware.operations.timeout import TimeoutMiddleware, TimeoutConfig
from fastx_middleware.operations.request_limit import (
    RequestLimitMiddleware,
    RequestLimitConfig,
)
from fastx_middleware.operations.trailing_slash import (
    TrailingSlashMiddleware,
    TrailingSlashConfig,
    SlashAction,
)
from fastx_middleware.operations.content_type import (
    ContentTypeMiddleware,
    ContentTypeConfig,
)
from fastx_middleware.operations.header_transform import (
    HeaderTransformMiddleware,
    HeaderTransformConfig,
)
from fastx_middleware.operations.request_validator import (
    RequestValidatorMiddleware,
    RequestValidatorConfig,
    ValidationRule,
)
from fastx_middleware.operations.json_schema import JSONSchemaMiddleware, JSONSchemaConfig
from fastx_middleware.operations.payload_size import (
    PayloadSizeMiddleware,
    PayloadSizeConfig,
)
from fastx_middleware.operations.method_override import (
    MethodOverrideMiddleware,
    MethodOverrideConfig,
)
from fastx_middleware.operations.request_fingerprint import (
    RequestFingerprintMiddleware,
    FingerprintConfig,
    get_fingerprint,
)
from fastx_middleware.operations.request_priority import (
    RequestPriorityMiddleware,
    PriorityConfig,
    Priority,
)

# ============================================================================
# URL & Routing
# ============================================================================
from fastx_middleware.operations.redirect import (
    RedirectMiddleware,
    RedirectConfig,
    RedirectRule,
)
from fastx_middleware.operations.path_rewrite import (
    PathRewriteMiddleware,
    PathRewriteConfig,
    RewriteRule,
)
from fastx_middleware.operations.proxy import ProxyMiddleware, ProxyConfig, ProxyRoute

# ============================================================================
# API Management
# ============================================================================
from fastx_middleware.operations.versioning import (
    VersioningMiddleware,
    VersioningConfig,
    VersionLocation,
    get_api_version,
)
from fastx_middleware.operations.deprecation import (
    DeprecationMiddleware,
    DeprecationConfig,
    DeprecationInfo,
)
from fastx_middleware.operations.retry_after import RetryAfterMiddleware, RetryAfterConfig
from fastx_middleware.operations.api_version_header import (
    APIVersionHeaderMiddleware,
    APIVersionHeaderConfig,
)

# ============================================================================
# Detection & Analytics
# ============================================================================
from fastx_middleware.operations.bot_detection import (
    BotDetectionMiddleware,
    BotConfig,
    BotAction,
)
from fastx_middleware.operations.geoip import GeoIPMiddleware, GeoIPConfig, get_geo_data
from fastx_middleware.operations.user_agent import (
    UserAgentMiddleware,
    UserAgentConfig,
    UserAgentInfo,
    get_user_agent,
)

# ============================================================================
# Feature Management & Testing
# ============================================================================
from fastx_middleware.operations.feature_flag import (
    FeatureFlagMiddleware,
    FeatureFlagConfig,
    get_feature_flags,
    is_feature_enabled,
)
from fastx_middleware.operations.ab_testing import (
    ABTestMiddleware,
    ABTestConfig,
    Experiment,
    get_variant,
)

# ============================================================================
# Localization & Content Negotiation
# ============================================================================
from fastx_middleware.operations.locale import LocaleMiddleware, LocaleConfig, get_locale
from fastx_middleware.operations.accept_language import (
    AcceptLanguageMiddleware,
    AcceptLanguageConfig,
    get_language,
)
from fastx_middleware.operations.content_negotiation import (
    ContentNegotiationMiddleware,
    ContentNegotiationConfig,
    get_negotiated_type,
)
from fastx_middleware.operations.client_hints import (
    ClientHintsMiddleware,
    ClientHintsConfig,
    get_client_hints,
)

# ============================================================================
# IP & Proxy Handling
# ============================================================================
from fastx_middleware.operations.real_ip import (
    RealIPMiddleware,
    RealIPConfig,
    get_real_ip,
)
from fastx_middleware.operations.xff_trust import XFFTrustMiddleware, XFFTrustConfig

# ============================================================================
# Observability, privacy & static asset caching
# ============================================================================
from fastx_middleware.operations.build_version import (
    BuildVersionMiddleware,
    BuildVersionConfig,
)
from fastx_middleware.operations.immutable_static_cache import (
    ImmutableStaticCacheMiddleware,
    ImmutableStaticCacheConfig,
)
from fastx_middleware.operations.edge_performance_tiers import (
    EdgePerformanceTier,
    EdgeTierCacheHeadersConfig,
    EdgeTierCacheHeadersMiddleware,
    EdgeTierDefinition,
    tier_definition,
)
from fastx_middleware.operations.dns_prefetch_control import (
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
