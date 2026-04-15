"""Item Service Dependency.

Returns a factory callable that, when invoked with request context and a
repository, produces an :class:`~services.item.item_service.ItemService`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from dependencies.services.v1.item.abstraction import IItemServiceDependency
from start_utils import logger


class ItemServiceDependency(IItemServiceDependency):
    """FastAPI dependency provider for ItemService."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating ItemService instances.

        Returns:
            Callable: Factory with signature
                ``factory(urn, user_urn, api_name, user_id, repository) -> ItemService``.
        """
        logger.debug("ItemServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            repository: Any = None,
        ) -> Any:
            """Create an ItemService instance with request context."""
            from services.item.item_service import ItemService

            logger.info("Instantiating ItemService")
            return ItemService(repository=repository)

        return factory


__all__ = ["ItemServiceDependency"]
