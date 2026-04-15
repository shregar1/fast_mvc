"""Fetch-User Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class FetchUserServiceDependency:
    """FastAPI dependency provider for FetchUserService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("FetchUserServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
        ) -> Any:
            from repositories.user.fetch import FetchUserRepository
            from services.user.fetch import FetchUserService

            return FetchUserService(
                repo=FetchUserRepository(),
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
            )

        return factory


__all__ = ["FetchUserServiceDependency"]
