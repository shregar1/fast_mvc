"""Default values for HTTP security headers (middleware / env-backed loaders).

Single source of truth for strings used by :mod:`utilities.security_headers` and
:class:`~dtos.configuration.security_headers.SecurityHeadersSettingsDTO` defaults.
"""

from __future__ import annotations

from typing import Final


class SecurityHeadersEnvVar:
    """Environment variable names for :mod:`utilities.security_headers` / ``SecurityHeadersMiddleware``."""

    X_CONTENT_TYPE_OPTIONS: Final[str] = "SECURITY_X_CONTENT_TYPE_OPTIONS"
    X_FRAME_OPTIONS: Final[str] = "SECURITY_X_FRAME_OPTIONS"
    X_XSS_PROTECTION: Final[str] = "SECURITY_X_XSS_PROTECTION"
    REFERRER_POLICY: Final[str] = "SECURITY_REFERRER_POLICY"
    ENABLE_HSTS: Final[str] = "SECURITY_ENABLE_HSTS"
    HSTS_MAX_AGE: Final[str] = "SECURITY_HSTS_MAX_AGE"
    HSTS_INCLUDE_SUBDOMAINS: Final[str] = "SECURITY_HSTS_INCLUDE_SUBDOMAINS"
    HSTS_PRELOAD: Final[str] = "SECURITY_HSTS_PRELOAD"
    CONTENT_SECURITY_POLICY: Final[str] = "SECURITY_CONTENT_SECURITY_POLICY"
    PERMISSIONS_POLICY: Final[str] = "SECURITY_PERMISSIONS_POLICY"
    CROSS_ORIGIN_OPENER_POLICY: Final[str] = "SECURITY_CROSS_ORIGIN_OPENER_POLICY"
    CROSS_ORIGIN_RESOURCE_POLICY: Final[str] = "SECURITY_CROSS_ORIGIN_RESOURCE_POLICY"
    CROSS_ORIGIN_EMBEDDER_POLICY: Final[str] = "SECURITY_CROSS_ORIGIN_EMBEDDER_POLICY"
    REMOVE_SERVER_HEADER: Final[str] = "SECURITY_REMOVE_SERVER_HEADER"


class SecurityHeadersConstants:
    """HTTP security header default strings (CSP, COOP, CORP, X-*, Referrer)."""

    DEFAULT_ENABLE_HSTS: Final[bool] = True
    DEFAULT_HSTS_MAX_AGE_SECONDS: Final[int] = 31_536_000
    DEFAULT_HSTS_INCLUDE_SUBDOMAINS: Final[bool] = True
    DEFAULT_HSTS_PRELOAD: Final[bool] = False
    DEFAULT_REMOVE_SERVER_HEADER: Final[bool] = True

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
