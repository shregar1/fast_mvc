"""User Login Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class UserLoginServiceDependency:
    """FastAPI dependency provider for UserLoginService.

    Returns a factory callable that controllers use to build a
    fully-configured service instance::

        service = factory(
            urn=..., user_urn=..., api_name=..., user_id=...,
            jwt_utility=..., user_repository=...,
            refresh_token_repository=...,
        )
        response_dto = service.run(request_dto=payload)
    """

    @staticmethod
    def derive() -> Callable:
        logger.debug("UserLoginServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            jwt_utility: Any = None,
            user_repository: Any = None,
            refresh_token_repository: Any = None,
        ) -> Any:
            from services.user.login import UserLoginService

            return UserLoginService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                user_repository=user_repository,
                jwt_utility=jwt_utility,
                refresh_token_repository=refresh_token_repository,
            )

        return factory


__all__ = ["UserLoginServiceDependency"]
