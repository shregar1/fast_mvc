"""Dependency Abstraction Module.

This module defines the I interface for FastAPI dependency injection.
Dependencies are reusable components that can be injected into route handlers,
providing services like database sessions, authentication, and utilities.

Example:
    >>> class DataIDependency(IDependency):
    ...     def __init__(self, urn: str):
    ...         super().__init__(urn=urn)
    ...         self.session = create_session()

"""

from __future__ import annotations

from abc import ABC
from typing import Any

from loguru import logger


class IDependency(ABC):
    """Abstract I class for FastAPI dependencies.

    The IDependency class provides a standardized interface for creating
    injectable dependencies in the FastX framework. Dependencies encapsulate
    reusable logic and resources that can be injected into route handlers.

    Common use cases:
        - DataI session management
        - Authentication/authorization
        - External API clients
        - Caching mechanisms
        - Rate limiting

    Attributes:
        urn (str | None): Unique Request Number for request tracing.
        user_urn (str | None): User's unique resource name.
        api_name (str | None): Name of the API endpoint using this dependency.
        user_id (str | None): DataI identifier of the authenticated user.
        logger: Structured logger bound with request context.

    Example:
        >>> class AuthDependency(IDependency):
        ...     def __init__(self, urn: str, user_urn: str):
        ...         super().__init__(urn=urn, user_urn=user_urn)
        ...
        ...     async def validate_token(self, token: str) -> bool:
        ...         # Token validation logic
        ...         return True

    """

    def __init__(
        self,
        urn: str | None = None,
        user_urn: str | None = None,
        api_name: str | None = None,
        user_id: int | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the dependency with request context.

        Args:
            urn (str, optional): Unique Request Number for tracing. Defaults to None.
            user_urn (str, optional): User's unique resource name. Defaults to None.
            api_name (str, optional): Name of the API endpoint. Defaults to None.
            user_id (str, optional): DataI ID of the user. Defaults to None.
            *args: Additional positional arguments for parent classes.
            **kwargs: Additional keyword arguments for parent classes.

        """
        super().__init__(*args, **kwargs)
        self._urn = urn
        self._user_urn = user_urn
        self._api_name = api_name
        self._user_id = user_id
        self._logger = logger.bind(
            urn=self._urn, user_urn=self._user_urn, api_name=self._api_name
        )

    @property
    def urn(self) -> str | None | None:
        """str | None: Get the Unique Request Number."""
        return self._urn

    @urn.setter
    def urn(self, value: str | None) -> None:
        """Set the Unique Request Number."""
        self._urn = value

    @property
    def user_urn(self) -> str | None:
        """str | None: Get the user's unique resource name."""
        return self._user_urn

    @user_urn.setter
    def user_urn(self, value: str | None) -> None:
        """Set the user's unique resource name."""
        self._user_urn = value

    @property
    def api_name(self) -> str | None:
        """str | None: Get the API endpoint name."""
        return self._api_name

    @api_name.setter
    def api_name(self, value: str | None) -> None:
        """Set the API endpoint name."""
        self._api_name = value

    @property
    def logger(self):
        """loguru.Logger: Get the structured logger instance."""
        return self._logger

    @logger.setter
    def logger(self, value) -> None:
        """Set the structured logger instance."""
        self._logger = value

    @property
    def user_id(self) -> str | None:
        """str | None: Get the user's database identifier."""
        return self._user_id

    @user_id.setter
    def user_id(self, value: str | None) -> None:
        """Set the user's database identifier."""
        self._user_id = value
