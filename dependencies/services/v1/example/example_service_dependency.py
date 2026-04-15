"""Example Service Dependency.

Returns a factory callable that, when invoked with request context and a
repository, produces an :class:`~services.example.example_service.ExampleService`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from dependencies.services.v1.example.abstraction import IExampleServiceDependency
from start_utils import logger


class ExampleServiceDependency(IExampleServiceDependency):
    """FastAPI dependency provider for ExampleService."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating ExampleService instances.

        Returns:
            Callable: Factory with signature
                ``factory(urn, user_urn, api_name, user_id, example_repo) -> ExampleService``.
        """
        logger.debug("ExampleServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            example_repo: Any = None,
        ) -> Any:
            """Create an ExampleService instance with request context."""
            from services.example.example_service import ExampleService

            logger.info("Instantiating ExampleService")
            return ExampleService(
                example_repo=example_repo,
                urn=urn,
                user_urn=user_urn,
                api_name=api_name or "example_api",
                user_id=user_id,
            )

        return factory


__all__ = ["ExampleServiceDependency"]
