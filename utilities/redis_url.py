"""Build ``REDIS_URL`` from ``REDIS_*`` environment variables."""

from __future__ import annotations

import os
from urllib.parse import quote

from constants.environment import EnvironmentVar

__all__ = ["build_redis_url_from_components", "resolve_redis_url"]


def build_redis_url_from_components() -> str | None:
    """Return a ``redis://`` URL from components, or ``None`` if host is missing."""
    host = (os.getenv(EnvironmentVar.REDIS_HOST) or "").strip()
    if not host:
        return None
    port = (os.getenv(EnvironmentVar.REDIS_PORT) or "").strip() or "6379"
    password = os.getenv(EnvironmentVar.REDIS_PASSWORD)
    if password is None:
        password = ""
    db = (os.getenv(EnvironmentVar.REDIS_DB) or "").strip() or "0"
    auth = f":{quote(str(password), safe='')}@" if password else ""
    return f"redis://{auth}{host}:{port}/{db}"


def resolve_redis_url() -> str:
    """Prefer explicit ``REDIS_URL``; otherwise build from ``REDIS_*``."""
    explicit = (os.getenv(EnvironmentVar.REDIS_URL) or "").strip()
    if explicit:
        return explicit
    built = build_redis_url_from_components()
    return built if built else ""
