"""
SPA-friendly CORS preset as a Pydantic DTO for Starlette :class:`CORSMiddleware`.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class CORSPreset(BaseModel):
    """
    Common single-page-app defaults: local dev origins, credentials, wide methods.

    Pass :meth:`starlette_kwargs` to ``app.add_middleware(CORSMiddleware, **kwargs)``.
    """

    allow_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        description="Allowed browser origins (exact match; use env-specific lists in prod).",
    )
    allow_credentials: bool = True
    allow_methods: list[str] = Field(
        default_factory=lambda: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    )
    allow_headers: list[str] = Field(default_factory=lambda: ["*"])
    expose_headers: list[str] = Field(default_factory=list)
    max_age: int = 600

    def starlette_kwargs(self) -> dict:
        """Keyword arguments for :class:`starlette.middleware.cors.CORSMiddleware`."""
        return {
            "allow_origins": list(self.allow_origins),
            "allow_credentials": self.allow_credentials,
            "allow_methods": list(self.allow_methods),
            "allow_headers": list(self.allow_headers),
            "expose_headers": list(self.expose_headers),
            "max_age": self.max_age,
        }
