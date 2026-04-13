"""User Subscription Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class UserSubscriptionServiceDependency:
    """FastAPI dependency provider for UserSubscriptionService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("UserSubscriptionServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            subscription_repository: Any = None,
        ) -> Any:
            from services.user.subscription import UserSubscriptionService

            return UserSubscriptionService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                subscription_repository=subscription_repository,
            )

        return factory


__all__ = ["UserSubscriptionServiceDependency"]
