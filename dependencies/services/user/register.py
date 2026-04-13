"""User Registration Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class UserRegistrationServiceDependency:
    """FastAPI dependency provider for UserRegistrationService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("UserRegistrationServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            user_repository: Any = None,
        ) -> Any:
            from services.user.register import UserRegistrationService

            return UserRegistrationService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                user_repository=user_repository,
            )

        return factory


__all__ = ["UserRegistrationServiceDependency"]
