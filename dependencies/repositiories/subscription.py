"""Subscription Repository Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class SubscriptionRepositoryDependency:
    """FastAPI dependency provider for SubscriptionRepository."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating SubscriptionRepository instances."""
        logger.debug("SubscriptionRepositoryDependency factory created")

        def factory(session: Any = None, **kwargs: Any) -> Any:
            from repositories.user.subscription_repository import SubscriptionRepository

            return SubscriptionRepository(session=session, **kwargs)

        return factory


__all__ = ["SubscriptionRepositoryDependency"]
