"""HTTP request helpers."""

from __future__ import annotations

from typing import Any


def get_client_ip(request: Any) -> str:
    """Extract the real client IP from a FastAPI / Starlette request.

    Checks ``X-Forwarded-For`` first, falls back to ``request.client.host``.
    """
    forwarded = getattr(request, "headers", {}).get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    client = getattr(request, "client", None)
    if client:
        return client.host
    return "unknown"


__all__ = ["get_client_ip"]
