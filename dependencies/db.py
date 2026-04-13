"""Database Dependency Module.

Provides ``DBDependency`` for FastAPI ``Depends()``.
Yields a fresh SQLAlchemy session per request and ensures cleanup.

Usage:
    >>> from fastapi import Depends
    >>> from dependencies.db import DBDependency
    >>>
    >>> async def my_endpoint(session = Depends(DBDependency.derive)):
    ...     ...
"""

from __future__ import annotations

from typing import Any, Generator

from start_utils import db_session_factory


class DBDependency:
    """FastAPI dependency provider for SQLAlchemy sessions."""

    @staticmethod
    def derive() -> Generator[Any, None, None]:
        """Yield a fresh session per request; close always."""
        if db_session_factory is None:
            yield None
            return
        session = db_session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


DatabaseDependency = DBDependency

__all__ = ["DBDependency"]
