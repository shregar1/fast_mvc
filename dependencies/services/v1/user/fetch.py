"""Fetch User Service Dependency.

Returns a factory callable that, when invoked with request context, produces
a :class:`~services.user.fetch.FetchUserService`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from dependencies.services.v1.user.abstraction import IUserServiceDependency
from start_utils import logger


class FetchUserServiceDependency(IUserServiceDependency):
    """FastAPI dependency provider for FetchUserService."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating FetchUserService instances.

        Returns:
            Callable: Factory with signature
                ``factory(urn, user_urn, api_name, user_id, repo) -> FetchUserService``.
        """
        logger.debug("FetchUserServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            repo: Any = None,
        ) -> Any:
            """Create a FetchUserService instance with request context."""
            from repositories.user.fetch import FetchUserRepository
            from services.user.fetch import FetchUserService

            logger.info("Instantiating FetchUserService")
            return FetchUserService(
                repo=repo or FetchUserRepository(urn=urn),
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
            )

        return factory


__all__ = ["FetchUserServiceDependency"]
