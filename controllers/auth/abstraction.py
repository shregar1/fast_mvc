"""Abstraction for auth-related controllers."""

from __future__ import annotations

from typing import Any

from controllers.abstraction import IController


class IAuthController(IController):
    """Interface for authentication and authorization controllers."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the auth controller base.

        Args:
            urn: Unique Request Number for tracing. Defaults to None.
            user_urn: User's URN. Defaults to None.
            api_name: API name. Defaults to None.
            user_id: User's database ID. Defaults to None.
            **kwargs: Forwarded to :class:`IController`.

        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            **kwargs,
        )
