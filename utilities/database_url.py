"""Build ``DATABASE_URL`` from ``DATABASE_*`` environment variables."""

from __future__ import annotations

import os
from urllib.parse import quote_plus

from constants.environment import EnvironmentVar

__all__ = ["build_postgresql_url_from_components", "resolve_database_url"]


def build_postgresql_url_from_components() -> str | None:
    """Return a ``postgresql://`` URL from components, or ``None`` if required parts are missing."""
    host = (os.getenv(EnvironmentVar.DATABASE_HOST) or "").strip()
    user = (os.getenv(EnvironmentVar.DATABASE_USER) or "").strip()
    database = (os.getenv(EnvironmentVar.DATABASE_NAME) or "").strip()
    if not host or not user or not database:
        return None
    port = (os.getenv(EnvironmentVar.DATABASE_PORT) or "").strip() or "5432"
    password = os.getenv(EnvironmentVar.DATABASE_PASSWORD)
    if password is None:
        password = ""
    return (
        f"postgresql://{quote_plus(user)}:{quote_plus(password)}"
        f"@{host}:{port}/{database}"
    )


def resolve_database_url() -> str:
    """Prefer explicit ``DATABASE_URL``; otherwise build from ``DATABASE_*``."""
    explicit = (os.getenv(EnvironmentVar.DATABASE_URL) or "").strip()
    if explicit:
        return explicit
    built = build_postgresql_url_from_components()
    return built if built else ""
