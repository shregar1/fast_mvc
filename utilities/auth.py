"""Authentication and authorization parsing utilities."""

from __future__ import annotations

import base64
import binascii
import secrets
from typing import Tuple


class AuthUtil:
    """Utility class for authentication and authorization parsing operations."""

    @staticmethod
    def parse_basic_authorization(header: str | None) -> Tuple[str, str] | None:
        """Parse HTTP Basic Authorization header.
        
        Args:
            header: The Authorization header value (e.g., "Basic dXNlcjpwYXNz").
            
        Returns:
            Tuple of (username, password) if valid, None otherwise.
        """
        if not header or not header.startswith("Basic "):
            return None
        try:
            raw = base64.b64decode(header[6:].strip())
            decoded = raw.decode("utf-8")
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
        return secrets.compare_digest(got.encode("utf-8"), expected.encode("utf-8"))


__all__ = ["AuthUtil"]
