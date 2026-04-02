"""Environment variable parsing utilities.

Provides type-safe helpers for reading environment variables with defaults.
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Any, Optional

from abstractions.utility import IUtility


class EnvironmentParserUtility(IUtility):
    """Parser for environment variables with type-safe conversion and defaults."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the environment parser.

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
    def parse_bool(name: str, default: bool) -> bool:
        """Parse environment variable as boolean.

        Values considered True: 'true', '1', 'yes', 'on' (case-insensitive).

        Args:
            name: Environment variable name.
            default: Default value if variable is not set.

        Returns:
            Boolean value of the environment variable.
        """
        raw = os.getenv(name)
        if raw is None:
            return default
        return raw.lower() in ("true", "1", "yes", "on")

    @staticmethod
    def parse_int(name: str, default: int) -> int:
        """Parse environment variable as integer.

        Args:
            name: Environment variable name.
            default: Default value if variable is not set or empty.

        Returns:
            Integer value of the environment variable.
        """
        raw = os.getenv(name)
        if raw is None or str(raw).strip() == "":
            return default
        return int(raw)

    @staticmethod
    def parse_str(name: str, default: str) -> str:
        """Parse environment variable as string.

        Args:
            name: Environment variable name.
            default: Default value if variable is not set.

        Returns:
            String value of the environment variable.
        """
        raw = os.getenv(name)
        if raw is None:
            return default
        return raw

    @staticmethod
    def parse_optional_str(name: str) -> str | None:
        """Parse environment variable as optional string.

        Returns None if the variable is not set or is empty/whitespace.

        Args:
            name: Environment variable name.

        Returns:
            String value or None if not set/empty.
        """
        raw = os.getenv(name)
        if raw is None or raw.strip() == "":
            return None
        return raw

    @staticmethod
    def parse_csv(name: str, default: Sequence[str]) -> list[str]:
        """Parse comma-separated environment variable as list of strings.

        Args:
            name: Environment variable name.
            default: Default sequence if variable is not set or empty.

        Returns:
            List of stripped, non-empty values from the environment variable.
        """
        raw = os.getenv(name)
        if raw is None or str(raw).strip() == "":
            return list(default)
        parts = [p.strip() for p in str(raw).split(",") if p.strip()]
        return parts if parts else list(default)

    @staticmethod
    def get_int_with_logging(name: str, default: int) -> int:
        """Get integer from environment variable with fallback and logging.

        Similar to parse_int but logs a warning when the value is invalid.

        Args:
            name: Environment variable name.
            default: Default value if variable is not set or invalid.

        Returns:
            Integer value of the environment variable.
        """
        value = os.getenv(name)
        if value is None:
            return default
        try:
            return int(value)
        except (TypeError, ValueError):
            # Import here to avoid circular dependency
            try:
                from loguru import logger

                logger.warning(
                    f"Invalid integer value for environment variable {name!r}: "
                    f"{value!r}. Falling back to default {default!r}."
                )
            except ImportError:
                pass
            return default

    @staticmethod
    def get_bool_with_logging(name: str, default: bool) -> bool:
        """Get boolean from environment variable with fallback and logging.

        Similar to parse_bool but logs a warning when the value is invalid.
        """
        value = os.getenv(name)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

__all__ = ["EnvironmentParserUtility"]
