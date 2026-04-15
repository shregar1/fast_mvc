"""Example Repository Dependency.

Returns a factory callable that, when invoked with request context, produces
an :class:`~repositories.example.ExampleRepository`.

Usage:
    >>> from fastapi import Depends
    >>> from dependencies.repositories.example import ExampleRepositoryDependency
    >>>
    >>> async def my_endpoint(
    ...     repo_factory: Callable = Depends(ExampleRepositoryDependency.derive),
    ... ):
    ...     repo = repo_factory(urn=urn, user_urn=user_urn, api_name="...", user_id=user_id)
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from dependencies.repositories.abstraction import IRepositoryDependency
from start_utils import logger


class ExampleRepositoryDependency(IRepositoryDependency):
    """FastAPI dependency provider for ExampleRepository."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating ExampleRepository instances.

        Returns:
            Callable: Factory with signature
                ``factory(urn, user_urn, api_name, user_id) -> ExampleRepository``.
        """
        logger.debug("ExampleRepositoryDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
        ) -> Any:
            """Create an ExampleRepository instance with request context."""
            from repositories.example import ExampleRepository

            logger.info("Instantiating ExampleRepository")
            return ExampleRepository(urn=urn)

        return factory


__all__ = ["ExampleRepositoryDependency"]
