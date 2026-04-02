"""String parsing and manipulation utilities."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Optional

from abstractions.utility import IUtility


class StringUtility(IUtility):
    """Utility class for string parsing and manipulation operations."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the string utility.

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
    def split_csv(value: str | None, default: Sequence[str]) -> list[str]:
        """Split a comma-separated string into a list of stripped, non-empty values.

        Args:
            value: Comma-separated string to split, or None.
            default: Default sequence if value is None or empty.

        Returns:
            List of stripped, non-empty string parts.
        """
        if value is None or str(value).strip() == "":
            return list(default)
        parts = [p.strip() for p in str(value).split(",") if p.strip()]
        return parts if parts else list(default)

    @staticmethod
    def normalize_path(value: str, *, leading_slash: bool = True) -> str:
        """Normalize a URL path.

        Ensures the path starts with a leading slash if leading_slash is True.

        Args:
            value: The path string to normalize.
            leading_slash: If True, ensure path starts with "/".

        Returns:
            Normalized path string.
        """
        if leading_slash and not value.startswith("/"):
            return "/" + value
        return value


__all__ = ["StringUtility"]
