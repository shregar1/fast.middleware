# API Reference

Complete API reference for FastMVC Middleware v0.5.0.

## Installation

```bash
pip install fast-middleware           # Core
pip install fast-middleware[jwt]      # With JWT support
pip install fast-middleware[proxy]    # With proxy support
pip install fast-middleware[all]      # All dependencies

```

## Quick Import

```python
from fastmiddleware import (
    # Most commonly used
    CORSMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    AuthenticationMiddleware,
    LoggingMiddleware,
    HealthCheckMiddleware,
    CompressionMiddleware,
)

```

---

## All Exports

### Base Class

| Export | Type | Description |
| -------- | ------ | ------------- |
| `FastMVCMiddleware` | Class | Base class for custom middleware |

### Security (14)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `SecurityHeadersMiddleware` | Middleware | Security headers |
| `SecurityHeadersConfig` | Dataclass | Config for SecurityHeadersMiddleware |
| `CORSMiddleware` | Middleware | Cross-origin resource sharing |
| `CSRFMiddleware` | Middleware | CSRF protection |
| `CSRFConfig` | Dataclass | Config for CSRFMiddleware |
| `HTTPSRedirectMiddleware` | Middleware | HTTP to HTTPS redirect |
| `HTTPSRedirectConfig` | Dataclass | Config for HTTPSRedirectMiddleware |
| `IPFilterMiddleware` | Middleware | IP whitelist/blacklist |
| `IPFilterConfig` | Dataclass | Config for IPFilterMiddleware |
| `TrustedHostMiddleware` | Middleware | Host header validation |
| `OriginMiddleware` | Middleware | Origin header validation |
| `OriginConfig` | Dataclass | Config for OriginMiddleware |
| `WebhookMiddleware` | Middleware | Webhook signature validation |
| `WebhookConfig` | Dataclass | Config for WebhookMiddleware |
| `ReferrerPolicyMiddleware` | Middleware | Referrer-Policy header |
| `ReferrerPolicyConfig` | Dataclass | Config for ReferrerPolicyMiddleware |
| `PermissionsPolicyMiddleware` | Middleware | Permissions-Policy header |
| `PermissionsPolicyConfig` | Dataclass | Config for PermissionsPolicyMiddleware |
| `CSPReportMiddleware` | Middleware | CSP violation reports |
| `CSPReportConfig` | Dataclass | Config for CSPReportMiddleware |
| `HoneypotMiddleware` | Middleware | Honeypot traps |
| `HoneypotConfig` | Dataclass | Config for HoneypotMiddleware |
| `SanitizationMiddleware` | Middleware | Input sanitization |
| `SanitizationConfig` | Dataclass | Config for SanitizationMiddleware |
| `ReplayPreventionMiddleware` | Middleware | Replay attack prevention |
| `ReplayPreventionConfig` | Dataclass | Config for ReplayPreventionMiddleware |
| `RequestSigningMiddleware` | Middleware | HMAC request signing |
| `RequestSigningConfig` | Dataclass | Config for RequestSigningMiddleware |

### Authentication (10)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `AuthenticationMiddleware` | Middleware | Pluggable auth |
| `AuthConfig` | Dataclass | Config for AuthenticationMiddleware |
| `AuthBackend` | ABC | Auth backend interface |
| `JWTAuthBackend` | Class | JWT auth backend |
| `APIKeyAuthBackend` | Class | API key auth backend |
| `BasicAuthMiddleware` | Middleware | HTTP Basic auth |
| `BasicAuthConfig` | Dataclass | Config for BasicAuthMiddleware |
| `BearerAuthMiddleware` | Middleware | Bearer token auth |
| `BearerAuthConfig` | Dataclass | Config for BearerAuthMiddleware |
| `ScopeMiddleware` | Middleware | OAuth scope validation |
| `ScopeConfig` | Dataclass | Config for ScopeMiddleware |
| `RouteAuthMiddleware` | Middleware | Per-route auth |
| `RouteAuthConfig` | Dataclass | Config for RouteAuthMiddleware |
| `RouteAuth` | Dataclass | Route auth requirement |

### Session & Context (20+)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `SessionMiddleware` | Middleware | Server-side sessions |
| `SessionConfig` | Dataclass | Config |
| `SessionStore` | ABC | Session store interface |
| `InMemorySessionStore` | Class | In-memory session store |
| `Session` | Class | Session object |
| `RequestContextMiddleware` | Middleware | Async context |
| `get_request_id` | Function | Get current request ID |
| `get_request_context` | Function | Get request context |
| `CorrelationMiddleware` | Middleware | Correlation IDs |
| `CorrelationConfig` | Dataclass | Config |
| `get_correlation_id` | Function | Get correlation ID |
| `TenantMiddleware` | Middleware | Multi-tenancy |
| `TenantConfig` | Dataclass | Config |
| `get_tenant` | Function | Get tenant object |
| `get_tenant_id` | Function | Get tenant ID |
| `ContextMiddleware` | Middleware | Shared context |
| `ContextConfig` | Dataclass | Config |
| `get_context` | Function | Get full context |
| `get_context_value` | Function | Get context value |
| `set_context_value` | Function | Set context value |
| `RequestIDPropagationMiddleware` | Middleware | ID propagation |
| `RequestIDPropagationConfig` | Dataclass | Config |
| `get_request_ids` | Function | Get ID chain |
| `get_trace_header` | Function | Get trace header value |

### Rate Limiting & Protection (10)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `RateLimitMiddleware` | Middleware | Rate limiting |
| `RateLimitConfig` | Dataclass | Config |
| `RateLimitStore` | ABC | Store interface |
| `InMemoryRateLimitStore` | Class | In-memory store |
| `QuotaMiddleware` | Middleware | Usage quotas |
| `QuotaConfig` | Dataclass | Config |
| `LoadSheddingMiddleware` | Middleware | Load shedding |
| `LoadSheddingConfig` | Dataclass | Config |
| `BulkheadMiddleware` | Middleware | Bulkhead pattern |
| `BulkheadConfig` | Dataclass | Config |
| `RequestDedupMiddleware` | Middleware | Request dedup |
| `RequestDedupConfig` | Dataclass | Config |
| `RequestCoalescingMiddleware` | Middleware | Request coalescing |
| `CoalescingConfig` | Dataclass | Config |

### Observability (20+)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `LoggingMiddleware` | Middleware | Request logging |
| `TimingMiddleware` | Middleware | Response timing |
| `RequestIDMiddleware` | Middleware | Request ID |
| `MetricsMiddleware` | Middleware | Prometheus metrics |
| `MetricsConfig` | Dataclass | Config |
| `MetricsCollector` | Class | Metrics collector |
| `ProfilingMiddleware` | Middleware | Profiling |
| `ProfilingConfig` | Dataclass | Config |
| `AuditMiddleware` | Middleware | Audit logging |
| `AuditConfig` | Dataclass | Config |
| `AuditEvent` | Dataclass | Audit event |
| `ResponseTimeMiddleware` | Middleware | SLA monitoring |
| `ResponseTimeConfig` | Dataclass | Config |
| `ResponseTimeSLA` | Dataclass | SLA definition |
| `ServerTimingMiddleware` | Middleware | Server-Timing |
| `ServerTimingConfig` | Dataclass | Config |
| `timing` | Function | Timing context manager |
| `add_timing` | Function | Add timing entry |
| `RequestLoggerMiddleware` | Middleware | Access logging |
| `RequestLoggerConfig` | Dataclass | Config |
| `CostTrackingMiddleware` | Middleware | Cost tracking |
| `CostTrackingConfig` | Dataclass | Config |
| `get_request_cost` | Function | Get request cost |
| `add_cost` | Function | Add cost |
| `RequestSamplerMiddleware` | Middleware | Request sampling |
| `RequestSamplerConfig` | Dataclass | Config |
| `is_sampled` | Function | Check if sampled |

### Performance (15)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `CompressionMiddleware` | Middleware | GZip compression |
| `CompressionConfig` | Dataclass | Config |
| `CacheMiddleware` | Middleware | HTTP caching |
| `CacheConfig` | Dataclass | Config |
| `ETagMiddleware` | Middleware | ETag generation |
| `ETagConfig` | Dataclass | Config |
| `ResponseCacheMiddleware` | Middleware | In-memory cache |
| `ResponseCacheConfig` | Dataclass | Config |
| `BandwidthMiddleware` | Middleware | Bandwidth throttling |
| `BandwidthConfig` | Dataclass | Config |
| `NoCacheMiddleware` | Middleware | No-cache headers |
| `NoCacheConfig` | Dataclass | Config |
| `ConditionalRequestMiddleware` | Middleware | If-None-Match |
| `ConditionalRequestConfig` | Dataclass | Config |
| `EarlyHintsMiddleware` | Middleware | HTTP 103 |
| `EarlyHintsConfig` | Dataclass | Config |
| `EarlyHint` | Dataclass | Hint definition |
| `ResponseSignatureMiddleware` | Middleware | Response signing |
| `ResponseSignatureConfig` | Dataclass | Config |
| `HATEOASMiddleware` | Middleware | Hypermedia links |
| `HATEOASConfig` | Dataclass | Config |
| `Link` | Dataclass | Hypermedia link |

### Error Handling (5)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `ErrorHandlerMiddleware` | Middleware | Error formatting |
| `ErrorConfig` | Dataclass | Config |
| `CircuitBreakerMiddleware` | Middleware | Circuit breaker |
| `CircuitBreakerConfig` | Dataclass | Config |
| `CircuitState` | Enum | Circuit states |
| `ExceptionHandlerMiddleware` | Middleware | Exception handlers |
| `ExceptionHandlerConfig` | Dataclass | Config |

### Operations (10)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `HealthCheckMiddleware` | Middleware | Health endpoints |
| `HealthConfig` | Dataclass | Config |
| `MaintenanceMiddleware` | Middleware | Maintenance mode |
| `MaintenanceConfig` | Dataclass | Config |
| `WarmupMiddleware` | Middleware | Container warmup |
| `WarmupConfig` | Dataclass | Config |
| `GracefulShutdownMiddleware` | Middleware | Graceful shutdown |
| `GracefulShutdownConfig` | Dataclass | Config |
| `ChaosMiddleware` | Middleware | Chaos engineering |
| `ChaosConfig` | Dataclass | Config |
| `SlowResponseMiddleware` | Middleware | Artificial delays |
| `SlowResponseConfig` | Dataclass | Config |

### API Management (12)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `VersioningMiddleware` | Middleware | API versioning |
| `VersioningConfig` | Dataclass | Config |
| `VersionLocation` | Enum | Version location |
| `get_api_version` | Function | Get API version |
| `DeprecationMiddleware` | Middleware | Deprecation |
| `DeprecationConfig` | Dataclass | Config |
| `DeprecationInfo` | Dataclass | Deprecation info |
| `RetryAfterMiddleware` | Middleware | Retry-After |
| `RetryAfterConfig` | Dataclass | Config |
| `APIVersionHeaderMiddleware` | Middleware | Version headers |
| `APIVersionHeaderConfig` | Dataclass | Config |
| `ContentNegotiationMiddleware` | Middleware | Content negotiation |
| `ContentNegotiationConfig` | Dataclass | Config |
| `get_negotiated_type` | Function | Get content type |
| `JSONSchemaMiddleware` | Middleware | JSON Schema |
| `JSONSchemaConfig` | Dataclass | Config |

### Detection (10)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `BotDetectionMiddleware` | Middleware | Bot detection |
| `BotConfig` | Dataclass | Config |
| `BotAction` | Enum | Bot actions |
| `UserAgentMiddleware` | Middleware | UA parsing |
| `UserAgentConfig` | Dataclass | Config |
| `UserAgentInfo` | Dataclass | Parsed UA |
| `get_user_agent` | Function | Get UA info |
| `GeoIPMiddleware` | Middleware | GeoIP |
| `GeoIPConfig` | Dataclass | Config |
| `get_geo_data` | Function | Get geo data |
| `ClientHintsMiddleware` | Middleware | Client Hints |
| `ClientHintsConfig` | Dataclass | Config |
| `get_client_hints` | Function | Get hints |
| `RequestFingerprintMiddleware` | Middleware | Fingerprinting |
| `FingerprintConfig` | Dataclass | Config |
| `get_fingerprint` | Function | Get fingerprint |

### Feature Management (8)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `FeatureFlagMiddleware` | Middleware | Feature flags |
| `FeatureFlagConfig` | Dataclass | Config |
| `get_feature_flags` | Function | Get all flags |
| `is_feature_enabled` | Function | Check flag |
| `ABTestMiddleware` | Middleware | A/B testing |
| `ABTestConfig` | Dataclass | Config |
| `Experiment` | Dataclass | Experiment definition |
| `get_variant` | Function | Get variant |

### Localization (6)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `LocaleMiddleware` | Middleware | Locale detection |
| `LocaleConfig` | Dataclass | Config |
| `get_locale` | Function | Get locale |
| `AcceptLanguageMiddleware` | Middleware | Language negotiation |
| `AcceptLanguageConfig` | Dataclass | Config |
| `get_language` | Function | Get language |

### Routing (12)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `RedirectMiddleware` | Middleware | Redirects |
| `RedirectConfig` | Dataclass | Config |
| `RedirectRule` | Dataclass | Redirect rule |
| `PathRewriteMiddleware` | Middleware | Path rewriting |
| `PathRewriteConfig` | Dataclass | Config |
| `RewriteRule` | Dataclass | Rewrite rule |
| `ProxyMiddleware` | Middleware | Reverse proxy |
| `ProxyConfig` | Dataclass | Config |
| `ProxyRoute` | Dataclass | Proxy route |
| `MethodOverrideMiddleware` | Middleware | Method override |
| `MethodOverrideConfig` | Dataclass | Config |
| `TrailingSlashMiddleware` | Middleware | Trailing slash |
| `TrailingSlashConfig` | Dataclass | Config |
| `SlashAction` | Enum | Slash actions |
| `HeaderTransformMiddleware` | Middleware | Header transform |
| `HeaderTransformConfig` | Dataclass | Config |
| `ContentTypeMiddleware` | Middleware | Content-Type |
| `ContentTypeConfig` | Dataclass | Config |

### IP & Proxy (4)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `RealIPMiddleware` | Middleware | Real IP |
| `RealIPConfig` | Dataclass | Config |
| `get_real_ip` | Function | Get real IP |
| `XFFTrustMiddleware` | Middleware | XFF trust |
| `XFFTrustConfig` | Dataclass | Config |

### Request Processing (15)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `TimeoutMiddleware` | Middleware | Timeout |
| `TimeoutConfig` | Dataclass | Config |
| `RequestLimitMiddleware` | Middleware | Body size limit |
| `RequestLimitConfig` | Dataclass | Config |
| `PayloadSizeMiddleware` | Middleware | Payload limits |
| `PayloadSizeConfig` | Dataclass | Config |
| `RequestValidatorMiddleware` | Middleware | Request validation |
| `RequestValidatorConfig` | Dataclass | Config |
| `ValidationRule` | Dataclass | Validation rule |
| `RequestFingerprintMiddleware` | Middleware | Fingerprinting |
| `FingerprintConfig` | Dataclass | Config |
| `get_fingerprint` | Function | Get fingerprint |
| `RequestPriorityMiddleware` | Middleware | Priority |
| `PriorityConfig` | Dataclass | Config |
| `Priority` | Enum | Priority levels |

### Other (10)

| Export | Type | Description |
| -------- | ------ | ------------- |
| `IdempotencyMiddleware` | Middleware | Idempotency |
| `IdempotencyConfig` | Dataclass | Config |
| `IdempotencyStore` | ABC | Store interface |
| `InMemoryIdempotencyStore` | Class | In-memory store |
| `DataMaskingMiddleware` | Middleware | Data masking |
| `DataMaskingConfig` | Dataclass | Config |
| `MaskingRule` | Dataclass | Masking rule |

---

## Module Metadata

```python
import fastmiddleware

print(fastmiddleware.__version__)  # "0.5.0"
print(fastmiddleware.__author__)   # "Shiv"
print(fastmiddleware.__email__)    # "sengarsinghshivansh@gmail.com, sengarsinghshreyansh@gmail.com"
print(fastmiddleware.__license__)  # "MIT"
print(fastmiddleware.__url__)      # "https://github.com/shregar1/fast-middleware"

```
