"""Abstraction for v1 API controllers."""

from __future__ import annotations

from typing import Any, Optional

from controllers.apis.abstraction import IAPIController


class IAPIV1Controller(IAPIController):
    """Interface for v1 API controllers."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the v1 API controller base.

        Args:
            urn: Unique Request Number for tracing. Defaults to None.
            user_urn: User's URN. Defaults to None.
            api_name: API name. Defaults to None.
            user_id: User's database ID. Defaults to None.
            **kwargs: Forwarded to :class:`IAPIController`.

        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            **kwargs,
        )


# Backward-compatible alias used by auth/user controllers.
IV1APIController = IAPIV1Controller
