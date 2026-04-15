"""Service Abstraction Module.

This module defines the I service interface that all business logic
services must inherit from. Services encapsulate domain logic and
orchestrate operations between repositories and external systems.

Example:
    >>> class UserRegistrationService(IService):
    ...     def __init__(self, user_repo: UserRepository, **kwargs):
    ...         super().__init__(**kwargs)
    ...         self.user_repo = user_repo
    ...
    ...     def run(self, request_dto: RegistrationDTO) -> dict:
    ...         # Business logic here
    ...         return {"status": "success"}

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from typing import Any

from pydantic import BaseModel
from core.utils.context import ContextMixin

if TYPE_CHECKING:
    from dtos.responses.base import BaseResponseDTO


class IService(ABC, ContextMixin):
    """Abstract I class for business logic services.

    The IService class provides a standardized interface for implementing
    business logic in the FastX framework. Services are the core of the
    application, containing domain rules and orchestrating data flow.

    Key responsibilities:
        - Implement business rules and validation
        - Coordinate between repositories and external APIs
        - Transform data between layers
        - Handle business-level error conditions

    Attributes:
        urn (str): Unique Request Number for tracing.
        user_urn (str): User's unique resource name.
        api_name (str): Name of the API endpoint.
        user_id (str | None): User identifier (aligned with :class:`~core.utils.context.ContextMixin`).
        logger: Structured logger bound with service context.

    Abstract Methods:
        run: Execute the service's main business logic.

    Example:
        >>> class OrderProcessingService(IService):
        ...     def __init__(self, order_repo, payment_client, **kwargs):
        ...         super().__init__(**kwargs)
        ...         self.order_repo = order_repo
        ...         self.payment_client = payment_client
        ...
        ...     def run(self, request_dto: OrderDTO) -> dict:
        ...         # Validate order
        ...         # Process payment
        ...         # Create order record
        ...         return {"order_id": "...", "status": "confirmed"}

    """

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the service with request context.

        Args:
            urn (str, optional): Unique Request Number for tracing. Defaults to None.
            user_urn (str, optional): User's unique resource name. Defaults to None.
            api_name (str, optional): Name of the API endpoint. Defaults to None.
            user_id (int, optional): DataI ID of the user. Defaults to None.
            *args: Additional positional arguments for parent classes.
            **kwargs: Additional keyword arguments for parent classes.

        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            *args,
            **kwargs,
        )

    @abstractmethod
    async def run(self, request_dto: BaseModel | None = None) -> "BaseResponseDTO":
        """Execute the service's main business logic (async).

        This is the primary entry point for the service. Subclasses must
        implement this coroutine to define their specific business operations.

        Args:
            request_dto (BaseModel | None): Pydantic model containing request
                data. Optional so services that take no request payload
                (e.g., status/read endpoints) can override with a zero-arg
                signature.

        Returns:
            BaseResponseDTO: Structured response envelope containing status,
                message, key, and any relevant data.

        Raises:
            IError: For business logic errors (subclass-specific).
            ValidationError: If request data validation fails.

        Example:
            >>> async def run(self, request_dto: UserDTO) -> BaseResponseDTO:
            ...     user = self.user_repo.find_by_email(request_dto.email)
            ...     if user:
            ...         raise BadInputError("Email already exists")
            ...     new_user = self.user_repo.create(request_dto)
            ...     return BaseResponseDTO(...)

        """
        pass
