"""Security headers middleware configuration (env → DTO → ``SecurityHeadersConfig``)."""

from __future__ import annotations

from fastmiddleware import SecurityHeadersConfig

from constants.security_headers import SecurityHeadersConstants
from dtos.configuration import SecurityHeadersSettingsDTO
from utilities.env import EnvironmentParser


class SecurityHeadersUtil:
    """Utility class for security headers middleware configuration."""

    @classmethod
    def load_settings_from_env(cls) -> SecurityHeadersSettingsDTO:
        """Load :class:`SecurityHeadersSettingsDTO` from ``SECURITY_*`` environment variables.

        All variables are optional; omitted values use the same defaults as the previous
        inline ``SecurityHeadersConfig`` in ``app.py``.

        Variables:
            ``SECURITY_X_CONTENT_TYPE_OPTIONS``, ``SECURITY_X_FRAME_OPTIONS``,
            ``SECURITY_X_XSS_PROTECTION``, ``SECURITY_REFERRER_POLICY``,
            ``SECURITY_ENABLE_HSTS``, ``SECURITY_HSTS_MAX_AGE``,
            ``SECURITY_HSTS_INCLUDE_SUBDOMAINS``, ``SECURITY_HSTS_PRELOAD``,
            ``SECURITY_CONTENT_SECURITY_POLICY`` (full CSP string; empty → built-in default),
            ``SECURITY_PERMISSIONS_POLICY``,
            ``SECURITY_CROSS_ORIGIN_OPENER_POLICY``, ``SECURITY_CROSS_ORIGIN_RESOURCE_POLICY``,
            ``SECURITY_CROSS_ORIGIN_EMBEDDER_POLICY``,
            ``SECURITY_REMOVE_SERVER_HEADER``.
        """
        csp = EnvironmentParser.parse_optional_str("SECURITY_CONTENT_SECURITY_POLICY")
        if csp is None:
            csp = SecurityHeadersConstants.CONTENT_SECURITY_POLICY

        coop = EnvironmentParser.parse_optional_str("SECURITY_CROSS_ORIGIN_OPENER_POLICY")
        if coop is None:
            coop = SecurityHeadersConstants.CROSS_ORIGIN_OPENER_POLICY

        corp = EnvironmentParser.parse_optional_str("SECURITY_CROSS_ORIGIN_RESOURCE_POLICY")
        if corp is None:
            corp = SecurityHeadersConstants.CROSS_ORIGIN_RESOURCE_POLICY

        return SecurityHeadersSettingsDTO(
            x_content_type_options=EnvironmentParser.parse_str(
                "SECURITY_X_CONTENT_TYPE_OPTIONS",
                SecurityHeadersConstants.X_CONTENT_TYPE_OPTIONS,
            ),
            x_frame_options=EnvironmentParser.parse_str(
                "SECURITY_X_FRAME_OPTIONS", SecurityHeadersConstants.X_FRAME_OPTIONS
            ),
            x_xss_protection=EnvironmentParser.parse_str(
                "SECURITY_X_XSS_PROTECTION", SecurityHeadersConstants.X_XSS_PROTECTION
            ),
            referrer_policy=EnvironmentParser.parse_str(
                "SECURITY_REFERRER_POLICY", SecurityHeadersConstants.REFERRER_POLICY
            ),
            enable_hsts=EnvironmentParser.parse_bool("SECURITY_ENABLE_HSTS", True),
            hsts_max_age=EnvironmentParser.parse_int("SECURITY_HSTS_MAX_AGE", 31_536_000),
            hsts_include_subdomains=EnvironmentParser.parse_bool("SECURITY_HSTS_INCLUDE_SUBDOMAINS", True),
            hsts_preload=EnvironmentParser.parse_bool("SECURITY_HSTS_PRELOAD", False),
            content_security_policy=csp,
            permissions_policy=EnvironmentParser.parse_optional_str("SECURITY_PERMISSIONS_POLICY"),
            cross_origin_opener_policy=coop,
            cross_origin_resource_policy=corp,
            cross_origin_embedder_policy=EnvironmentParser.parse_optional_str(
                "SECURITY_CROSS_ORIGIN_EMBEDDER_POLICY"
            ),
            remove_server_header=EnvironmentParser.parse_bool("SECURITY_REMOVE_SERVER_HEADER", True),
        )

    @classmethod
    def get_middleware_config(cls) -> SecurityHeadersConfig:
        """Return a :class:`SecurityHeadersConfig` for ``SecurityHeadersMiddleware``."""
        return cls.load_settings_from_env().to_middleware_config()


# Backward compatibility: module-level functions delegate to the class
load_security_headers_settings_from_env = SecurityHeadersUtil.load_settings_from_env
get_security_headers_middleware_config = SecurityHeadersUtil.get_middleware_config


__all__ = [
    "SecurityHeadersUtil",
    "load_security_headers_settings_from_env",
    "get_security_headers_middleware_config",
]
