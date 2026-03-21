# CSPReportMiddleware

Handle Content Security Policy violation reports.

## Installation

```bash
pip install fast-middleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import CSPReportMiddleware

app = FastAPI()

csp_reporter = CSPReportMiddleware(
    app,
    report_uri="/_csp-report",
    log_reports=True,
    store_reports=True,
)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `report_uri` | `str` | `"/_csp-report"` | Endpoint for CSP reports |
| `log_reports` | `bool` | `True` | Log reports to console |
| `store_reports` | `bool` | `False` | Store reports in memory |
| `max_stored` | `int` | `1000` | Max reports to store |

## Examples

### Basic CSP Reporting

```python
from fastmiddleware import CSPReportMiddleware, SecurityHeadersMiddleware

# Set up CSP with report-uri
app.add_middleware(
    SecurityHeadersMiddleware,
    content_security_policy="default-src 'self'; report-uri /_csp-report",
)

# Handle reports
csp_reporter = CSPReportMiddleware(
    app,
    report_uri="/_csp-report",
    log_reports=True,
)

```

### Store and Retrieve Reports

```python
csp_reporter = CSPReportMiddleware(
    app,
    store_reports=True,
    max_stored=500,
)

# Later, retrieve stored reports
@app.get("/admin/csp-reports")
async def get_reports():
    reports = csp_reporter.get_reports()
    return {"reports": reports, "count": len(reports)}

# Clear reports
@app.delete("/admin/csp-reports")
async def clear_reports():
    csp_reporter.clear_reports()
    return {"status": "cleared"}

```

### Custom Report Handler

```python
async def send_to_siem(report: dict):
    await siem_client.send_event("csp_violation", report)

csp_reporter = CSPReportMiddleware(
    app,
    report_uri="/_csp-report",
    handler=send_to_siem,
)

```

### Report-Only Mode

```python
app.add_middleware(
    SecurityHeadersMiddleware,
    content_security_policy_report_only="default-src 'self'; report-uri /_csp-report",
)

csp_reporter = CSPReportMiddleware(app)

```

## CSP Report Format

```json
{
    "csp-report": {
        "document-uri": "https://example.com/page",
        "referrer": "",
        "violated-directive": "script-src",
        "effective-directive": "script-src",
        "original-policy": "default-src 'self'; script-src 'self'",
        "blocked-uri": "https://evil.com/script.js",
        "status-code": 0
    }
}

```

## Methods

### `get_reports() -> list[dict]`

Get all stored CSP violation reports.

### `clear_reports() -> None`

Clear all stored reports.

### `get_stats() -> dict`

Get statistics about violations.

```python
stats = csp_reporter.get_stats()

# {"total": 150, "by_directive": {"script-src": 100, "style-src": 50}}

```

## Related Middlewares

- [SecurityHeadersMiddleware](security-headers.md) - Set CSP headers
- [LoggingMiddleware](logging.md) - Request logging
