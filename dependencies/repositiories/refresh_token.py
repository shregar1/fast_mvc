"""Refresh Token Repository Dependency.

Returns a factory callable that, when invoked with request context,
produces a :class:`~repositories.user.refresh_token_repository.RefreshTokenRepository`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class RefreshTokenRepositoryDependency:
    """FastAPI dependency provider for RefreshTokenRepository."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating RefreshTokenRepository instances.

        The factory signature matches what controllers expect::

            refresh_token_repo = factory(
                urn=..., user_urn=..., api_name=...,
                user_id=..., session=...,
            )
        """
        logger.debug("RefreshTokenRepositoryDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
        ) -> Any:
            from repositories.user.refresh_token_repository import RefreshTokenRepository

            return RefreshTokenRepository(session=session)

        return factory


__all__ = ["RefreshTokenRepositoryDependency"]
