"""v1 user service dependency abstraction."""

from __future__ import annotations

from typing import Any, Optional

from dependencies.services.v1.abstraction import IV1ServiceDependency


class IUserServiceDependency(IV1ServiceDependency):
    """Interface for v1 user-scoped service dependencies."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the v1 user service dependency base.

        Args:
            urn: Unique Request Number for tracing. Defaults to None.
            user_urn: User's URN. Defaults to None.
            api_name: API name. Defaults to None.
            user_id: User's database ID. Defaults to None.
            *args: Forwarded to parent.
            **kwargs: Forwarded to parent.

        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            *args,
            **kwargs,
        )
