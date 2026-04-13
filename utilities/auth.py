"""Authentication and authorization parsing utilities."""

from __future__ import annotations

import base64
import binascii
import secrets
from typing import Any, Optional, Tuple

from constants.http_header import HttpHeader
from abstractions.utility import IUtility


class AuthUtility(IUtility):
    """Utility class for authentication and authorization parsing operations."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the auth utility.

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
    def parse_basic_authorization(header: str | None) -> Tuple[str, str] | None:
        """Parse HTTP Basic Authorization header.

        Args:
            header: The Authorization header value (e.g., "Basic dXNlcjpwYXNz").

        Returns:
            Tuple of (username, password) if valid, None otherwise.
        """
        if not header or not header.startswith(HttpHeader.AUTHORIZATION_BASIC_PREFIX):
            return None
        try:
            raw = base64.b64decode(
                header[HttpHeader.AUTHORIZATION_BASIC_PREFIX_LENGTH:].strip()
            )
            decoded = raw.decode(HttpHeader.ENCODING_UTF8)
        except (binascii.Error, UnicodeDecodeError, ValueError):
            return None
        if ":" not in decoded:
            return None
        username, _, password = decoded.partition(":")
        return username, password

    @staticmethod
    def constant_time_compare(got: str, expected: str) -> bool:
        """Compare two strings in constant time to prevent timing attacks.

        Args:
            got: The provided string.
            expected: The expected string.

        Returns:
            True if strings match, False otherwise.
        """
        if len(got) != len(expected):
            return False
        return secrets.compare_digest(
            got.encode(HttpHeader.ENCODING_UTF8), expected.encode(HttpHeader.ENCODING_UTF8)
        )


__all__ = ["AuthUtility"]
