# MetricsMiddleware

Prometheus-compatible metrics collection with request counts, latency histograms, and custom metrics.

## Installation

```python
from fastmiddleware import MetricsMiddleware, MetricsConfig, MetricsCollector

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import MetricsMiddleware

app = FastAPI()
app.add_middleware(MetricsMiddleware)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `metrics_path` | `str` | `"/metrics"` | Metrics endpoint |
| `histogram_buckets` | `tuple` | Default buckets | Latency buckets |
| `path_patterns` | `dict` | `{}` | Path normalization |
| `enable_latency_histogram` | `bool` | `True` | Track latency |
| `enable_request_count` | `bool` | `True` | Count requests |

## Metrics Collected

| Metric | Type | Description |
| -------- | ------ | ------------- |
| `fastx_http_requests_total` | Counter | Total requests |
| `fastx_http_request_duration_seconds` | Histogram | Request latency |
| `fastx_http_response_size_bytes` | Summary | Response size |
| `fastx_http_errors_total` | Counter | 5xx errors |
| `fastx_uptime_seconds` | Gauge | Service uptime |

## Examples

### Basic Usage

```python
app.add_middleware(MetricsMiddleware)

# Access metrics at /metrics

```

### Custom Path

```python
config = MetricsConfig(metrics_path="/prometheus")
app.add_middleware(MetricsMiddleware, config=config)

```

### Path Normalization

```python
config = MetricsConfig(
    path_patterns={
        r"/users/\d+": "/users/{id}",
        r"/orders/[a-f0-9-]+": "/orders/{uuid}",
    },
)

```

## Prometheus Config

```yaml
scrape_configs:
  - job_name: 'fastmvc-app'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics

```

## Grafana Queries

```promql

# Request rate
rate(fastx_http_requests_total[5m])

# Error rate
rate(fastx_http_requests_total{status=~"5.."}[5m])

# P95 latency
histogram_quantile(0.95, rate(fastx_http_request_duration_seconds_bucket[5m]))

```
