"""Datetime utilities for consistent timezone handling."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from abstractions.utility import IUtility


class DateTimeUtility(IUtility):
    """Utility class for datetime operations with consistent timezone handling."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the datetime utility.

        Args:
            urn: Unique Request Number for tracing.
            user_urn: User's unique resource name.
            api_name: Name of the API endpoint.
            user_id: Database identifier of the user.
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

    @staticmethod
    def utc_now() -> datetime:
        """Return current UTC datetime with timezone info.

        Returns:
            Current UTC datetime with timezone.utc.
        """
        return datetime.now(timezone.utc)

    @staticmethod
    def utc_now_iso() -> str:
        """Return current UTC datetime as ISO format string.

        Returns:
            ISO 8601 formatted UTC datetime string.
        """
        return datetime.now(timezone.utc).isoformat()


__all__ = ["DateTimeUtility"]
