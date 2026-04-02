"""DataI Dependency Module.

Provides ``DBDependency`` for FastAPI ``Depends()`` (same pattern as ``CacheDependency``).

Usage:
    >>> from fastapi import Depends
    >>> from dependencies.db import DBDependency
    >>>
    >>> async def my_endpoint(session = Depends(DBDependency.derive)):
    ...     ...
"""

from __future__ import annotations

from typing import Any

from start_utils import db_session


class DBDependency:
    """FastAPI dependency provider for the shared SQLAlchemy session."""

    @staticmethod
    def derive() -> Any:
        """Return the application ``db_session`` or raise if DataI is not configured."""
        if db_session is None:
            raise ImportError(
                "fast_db is required for database dependencies. "
                "Install with: pip install fastx-mvc[platform]"
            )
        return db_session


DatabaseDependency = DBDependency

__all__ = ["DBDependency"]
