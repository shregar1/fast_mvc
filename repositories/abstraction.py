"""Application repository abstraction.

Inheritance: :class:`IRepository` → :class:`abstractions.repository.IRepository` →
:class:`core.utils.context.ContextMixin`.
"""

from __future__ import annotations

from typing import Any, Optional

from abstractions.repository import IRepository as FrameworkRepository


class IRepository(FrameworkRepository):
    """Root repository interface for this application."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        session: Any = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the application repository base.

        Args:
            urn: Unique Request Number for tracing. Defaults to None.
            user_urn: User's URN. Defaults to None.
            api_name: API name. Defaults to None.
            user_id: User's database ID. Defaults to None.
            session: Database session when applicable. Defaults to None.
            *args: Additional positional arguments for parent classes.
            **kwargs: Additional keyword arguments for parent classes.

        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            session=session,
            *args,
            **kwargs,
        )
