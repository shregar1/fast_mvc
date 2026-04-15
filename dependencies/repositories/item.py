"""Item Repository Dependency.

Returns a factory callable that, when invoked with request context, produces
an :class:`~repositories.item.ItemRepository`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from dependencies.repositories.abstraction import IRepositoryDependency
from start_utils import logger


class ItemRepositoryDependency(IRepositoryDependency):
    """FastAPI dependency provider for ItemRepository."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating ItemRepository instances.

        Returns:
            Callable: Factory with signature
                ``factory(urn, user_urn, api_name, user_id) -> ItemRepository``.
        """
        logger.debug("ItemRepositoryDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
        ) -> Any:
            """Create an ItemRepository instance (in-memory; URN for tracing)."""
            from repositories.item import ItemRepository

            logger.info("Instantiating ItemRepository")
            return ItemRepository()

        return factory


__all__ = ["ItemRepositoryDependency"]
