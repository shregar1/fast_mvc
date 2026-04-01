"""Datetime utilities for consistent timezone handling."""

from __future__ import annotations

from datetime import datetime, timezone


class DateTimeUtil:
    """Utility class for datetime operations with consistent timezone handling."""

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


__all__ = ["DateTimeUtil"]
