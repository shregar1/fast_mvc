"""Application service abstraction.

Inheritance: :class:`IService` → :class:`abstractions.service.IService` →
:class:`core.utils.context.ContextMixin`.
"""

from typing import Any, Optional

from abstractions.service import IService as FrameworkService


class IService(FrameworkService):
    """Root service interface for this application."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the application service base.

        Args:
            urn: Unique Request Number for tracing. Defaults to None.
            user_urn: User's URN. Defaults to None.
            api_name: API name. Defaults to None.
            user_id: User's database ID. Defaults to None.
            *args: Forwarded to the framework service.
            **kwargs: Forwarded to the framework service (e.g. ``logger``).

        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            *args,
            **kwargs,
        )
