"""Datetime utilities for consistent timezone handling."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from abstractions.utility import IUtility


class DateTimeUtility(IUtility):
    """Utility class for datetime operations with consistent timezone handling."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> None:
        """Initialize the datetime utility.

        Args:
            urn: Unique Request Number for tracing.
            user_urn: User's unique resource name.
            api_name: Name of the API endpoint.
            user_id: Database identifier of the user.
        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
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


# Backward compatibility: module-level functions delegate to the class
utc_now = DateTimeUtility.utc_now
utc_now_iso = DateTimeUtility.utc_now_iso


__all__ = [
    "DateTimeUtility",
    "utc_now",
    "utc_now_iso",
]
