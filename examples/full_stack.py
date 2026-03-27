"""Full stack example for FastMVC Middleware.

This example demonstrates a production-ready FastAPI application with:
- CORS handling
- Security headers
- Rate limiting
- JWT authentication
- Request logging
- Request context management

Run with: uvicorn examples.full_stack:app --reload
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from fastmiddleware import (
    CORSMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    RateLimitConfig,
    AuthenticationMiddleware,
    AuthConfig,
    APIKeyAuthBackend,
    LoggingMiddleware,
    TimingMiddleware,
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)


# ============================================================================
# Configuration
# ============================================================================

# In production, load from environment variables
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
API_KEYS = {"demo-api-key-1", "demo-api-key-2"}  # In production, use a database
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))


# ============================================================================
# Models
# ============================================================================


class Item(BaseModel):
    """Sample item model."""

    name: str
    description: Optional[str] = None
    price: float


class ItemResponse(BaseModel):
    """Response model for items."""

    id: int
    name: str
    description: Optional[str]
    price: float
    created_at: datetime


# ============================================================================
# Application Setup
# ============================================================================

app = FastAPI(
    title="Full Stack Middleware Example",
    description="Production-ready FastAPI application with comprehensive middleware",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ============================================================================
# Middleware Configuration (Order matters!)
# ============================================================================

# 1. Timing (outermost - measures total time including all middleware)
app.add_middleware(
    TimingMiddleware,
    header_name="X-Response-Time",
    include_unit=True,
)

# 2. Logging (logs all requests and responses)
app.add_middleware(
    LoggingMiddleware,
    exclude_paths={"/health", "/healthz", "/ready", "/metrics"},
    log_request_headers=False,  # Enable in debug mode
)

# 3. Security Headers (adds security headers to all responses)
app.add_middleware(
    SecurityHeadersMiddleware,
    enable_hsts=False,  # Enable in production with HTTPS
    content_security_policy="default-src 'self'",
)

# 4. Rate Limiting (protects against abuse)
rate_limit_config = RateLimitConfig(
    requests_per_minute=RATE_LIMIT_PER_MINUTE,
    requests_per_hour=1000,
)
app.add_middleware(
    RateLimitMiddleware,
    config=rate_limit_config,
    error_message="Too many requests. Please slow down.",
)

# 5. Authentication (validates API keys)
# Using API key auth for this example; JWT example below
api_key_backend = APIKeyAuthBackend(valid_keys=API_KEYS)
auth_config = AuthConfig(
    exclude_paths={
        "/",
        "/health",
        "/healthz",
        "/ready",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/public",
    },
    header_name="Authorization",
    header_scheme="Bearer",
    error_message="Invalid or missing API key",
)
app.add_middleware(
    AuthenticationMiddleware,
    backend=api_key_backend,
    config=auth_config,
)

# 6. Request Context (innermost - provides request tracking)
app.add_middleware(
    RequestContextMiddleware,
    request_id_header="X-Request-ID",
    process_time_header="X-Process-Time",
)

# 7. CORS (must be last added = first executed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=600,
)


# ============================================================================
# In-memory storage (replace with database in production)
# ============================================================================

items_db: dict[int, ItemResponse] = {}
item_counter = 0


# ============================================================================
# Routes
# ============================================================================


@app.get("/")
async def root():
    """Public root endpoint."""
    return {
        "message": "FastMVC Middleware Full Stack Example",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/ready")
async def readiness():
    """Readiness check endpoint."""
    return {"ready": True}


@app.get("/public")
async def public_endpoint():
    """Public endpoint that doesn't require authentication."""
    return {"message": "This is a public endpoint"}


@app.get("/protected")
async def protected_endpoint(request: Request):
    """Protected endpoint that requires authentication."""
    # Access auth data from middleware
    auth = request.state.auth

    # Access request context
    request_id = get_request_id()
    ctx = get_request_context()

    return {
        "message": "You are authenticated!",
        "auth": auth,
        "request_id": request_id,
        "client_ip": ctx.get("client_ip"),
    }


@app.get("/items")
async def list_items(request: Request):
    """List all items (protected)."""
    return {
        "items": list(items_db.values()),
        "count": len(items_db),
    }


@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item, request: Request):
    """Create a new item (protected)."""
    global item_counter
    item_counter += 1

    item_response = ItemResponse(
        id=item_counter,
        name=item.name,
        description=item.description,
        price=item.price,
        created_at=datetime.utcnow(),
    )

    items_db[item_counter] = item_response
    return item_response


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, request: Request):
    """Get an item by ID (protected)."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, request: Request):
    """Delete an item by ID (protected)."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return {"deleted": item_id}


@app.get("/debug/headers")
async def debug_headers(request: Request):
    """Debug endpoint showing all request headers (protected)."""
    return {
        "headers": dict(request.headers),
        "request_id": get_request_id(),
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("Starting server...")
    print(f"Allowed origins: {ALLOWED_ORIGINS}")
    print(f"Rate limit: {RATE_LIMIT_PER_MINUTE} requests/minute")
    print("API Documentation: http://localhost:8000/docs")
    print("\nTest with:")
    print("  curl http://localhost:8000/public")
    print(
        '  curl -H "Authorization: Bearer demo-api-key-1" http://localhost:8000/protected'
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
