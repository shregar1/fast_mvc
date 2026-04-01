"""String parsing and manipulation utilities."""

from __future__ import annotations

from collections.abc import Sequence


class StringUtil:
    """Utility class for string parsing and manipulation operations."""

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


# Backward compatibility: module-level functions delegate to the class
split_csv = StringUtil.split_csv
normalize_path = StringUtil.normalize_path


__all__ = [
    "StringUtil",
    "normalize_path",
    "split_csv",
]
