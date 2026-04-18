"""Authentication and authorization parsing utilities.

Module-level functions — stateless helpers, no class needed.
"""

from __future__ import annotations

import base64
import binascii
import secrets
from typing import Tuple

from constants.http_header import HttpHeader


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


__all__ = ["parse_basic_authorization", "constant_time_compare"]
