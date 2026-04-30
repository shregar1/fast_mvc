"""User Repository Dependency.

Returns a factory callable that, when invoked with request context,
produces a :class:`~fastx_database.repositories.user.UserRepository`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class UserRepositoryDependency:
    """FastAPI dependency provider for UserRepository."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating UserRepository instances.

        The factory signature matches what controllers expect::

            user_repository = factory(
                urn=..., user_urn=..., api_name=...,
                user_id=..., session=...,
            )
        """
        logger.debug("UserRepositoryDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
        ) -> Any:
            from repositories.user.user_repository import UserRepository

            return UserRepository(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                session=session,
            )

        return factory


__all__ = ["UserRepositoryDependency"]
