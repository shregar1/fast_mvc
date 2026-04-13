"""User Logout Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class UserLogoutServiceDependency:
    """FastAPI dependency provider for UserLogoutService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("UserLogoutServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            jwt_utility: Any = None,
            user_repository: Any = None,
            refresh_token_repository: Any = None,
            auth_token: str | None = None,
        ) -> Any:
            from services.user.logout import UserLogoutService

            return UserLogoutService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                user_repository=user_repository,
                jwt_utility=jwt_utility,
                refresh_token_repository=refresh_token_repository,
                auth_token=auth_token,
            )

        return factory


__all__ = ["UserLogoutServiceDependency"]
