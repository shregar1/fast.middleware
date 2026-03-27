"""Basic usage example for FastMVC Middleware.

This example demonstrates how to set up a simple FastAPI application
with essential middleware components.

Run with: uvicorn examples.basic_usage:app --reload
"""

from fastapi import FastAPI, Request
from fastmiddleware import (
    CORSMiddleware,
    LoggingMiddleware,
    TimingMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)

# Create FastAPI app
app = FastAPI(
    title="Basic Middleware Example",
    description="Demonstrates basic FastMVC middleware usage",
    version="1.0.0",
)

# Add middleware in order (first added = last executed)
# This means CORS runs first, then RequestID, then Security, etc.

# 1. Timing - measures total request time (outermost)
app.add_middleware(TimingMiddleware)

# 2. Logging - logs requests and responses
app.add_middleware(LoggingMiddleware)

# 3. Security Headers - adds security headers to all responses
app.add_middleware(SecurityHeadersMiddleware)

# 4. Request ID - generates unique ID for each request
app.add_middleware(RequestIDMiddleware)

# 5. CORS - handles cross-origin requests (runs first)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use specific origins
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,  # Must be False when using "*" origins
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello, World!", "status": "healthy"}


@app.get("/health")
async def health():
    """Health check endpoint (excluded from logging by default)."""
    return {"status": "healthy"}


@app.get("/request-info")
async def request_info(request: Request):
    """Shows request information including the generated request ID."""
    return {
        "request_id": getattr(request.state, "request_id", None),
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host if request.client else None,
    }


@app.post("/echo")
async def echo(request: Request):
    """Echo back the request body."""
    body = await request.json()
    return {"received": body}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
