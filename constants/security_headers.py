"""Default values for HTTP security headers (middleware / env-backed loaders).

Single source of truth for strings used by :mod:`utilities.security_headers` and
:class:`~dtos.configuration.security_headers.SecurityHeadersSettingsDTO` defaults.
"""

from __future__ import annotations

from typing import Final


class SecurityHeadersConstants:
    """HTTP security header default strings (CSP, COOP, CORP, X-*, Referrer)."""

    # Default CSP: self-hosted API + Swagger/ReDoc assets (jsdelivr, Google Fonts).
    CONTENT_SECURITY_POLICY: Final[str] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' data: https://fonts.gstatic.com; "
        "img-src 'self' data: https: blob:; "
        "connect-src 'self'"
    )

    CROSS_ORIGIN_OPENER_POLICY: Final[str] = "same-origin"
    CROSS_ORIGIN_RESOURCE_POLICY: Final[str] = "same-origin"

    X_CONTENT_TYPE_OPTIONS: Final[str] = "nosniff"
    X_FRAME_OPTIONS: Final[str] = "DENY"
    X_XSS_PROTECTION: Final[str] = "1; mode=block"
    REFERRER_POLICY: Final[str] = "strict-origin-when-cross-origin"
