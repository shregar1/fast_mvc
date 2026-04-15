"""Security headers middleware configuration (env → DTO → ``SecurityHeadersConfig``)."""

from __future__ import annotations

from typing import Any, Optional

from fast_middleware import SecurityHeadersConfig

from abstractions.utility import IUtility
from constants.security_headers import SecurityHeadersConstants, SecurityHeadersEnvVar
from dtos.configuration import SecurityHeadersSettingsDTO
from utilities.env import EnvironmentParserUtility


class SecurityHeadersUtility(IUtility):
    """Utility class for security headers middleware configuration."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the security headers utility.

        Args:
            urn: Unique Request Number for tracing.
            user_urn: User's unique resource name.
            api_name: Name of the API endpoint.
            user_id: Database identifier of the user.
            *args: Additional positional arguments forwarded to parent.
            **kwargs: Additional keyword arguments forwarded to parent.
        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            *args,
            **kwargs,
        )

    @classmethod
    def load_settings_from_env(cls) -> SecurityHeadersSettingsDTO:
        """Load :class:`SecurityHeadersSettingsDTO` from ``SECURITY_*`` environment variables.

        All variables are optional; omitted values use the same defaults as the previous
        inline ``SecurityHeadersConfig`` in ``app.py``.

        Variables:
            See :class:`constants.security_headers.SecurityHeadersEnvVar` for keys
            (``SECURITY_*``). Omitted values use :class:`~constants.security_headers.SecurityHeadersConstants`.
        """
        csp = EnvironmentParserUtility.parse_optional_str(
            SecurityHeadersEnvVar.CONTENT_SECURITY_POLICY
        )
        if csp is None:
            csp = SecurityHeadersConstants.CONTENT_SECURITY_POLICY

        coop = EnvironmentParserUtility.parse_optional_str(
            SecurityHeadersEnvVar.CROSS_ORIGIN_OPENER_POLICY
        )
        if coop is None:
            coop = SecurityHeadersConstants.CROSS_ORIGIN_OPENER_POLICY

        corp = EnvironmentParserUtility.parse_optional_str(
            SecurityHeadersEnvVar.CROSS_ORIGIN_RESOURCE_POLICY
        )
        if corp is None:
            corp = SecurityHeadersConstants.CROSS_ORIGIN_RESOURCE_POLICY

        return SecurityHeadersSettingsDTO(
            x_content_type_options=EnvironmentParserUtility.parse_str(
                SecurityHeadersEnvVar.X_CONTENT_TYPE_OPTIONS,
                SecurityHeadersConstants.X_CONTENT_TYPE_OPTIONS,
            ),
            x_frame_options=EnvironmentParserUtility.parse_str(
                SecurityHeadersEnvVar.X_FRAME_OPTIONS, SecurityHeadersConstants.X_FRAME_OPTIONS
            ),
            x_xss_protection=EnvironmentParserUtility.parse_str(
                SecurityHeadersEnvVar.X_XSS_PROTECTION,
                SecurityHeadersConstants.X_XSS_PROTECTION,
            ),
            referrer_policy=EnvironmentParserUtility.parse_str(
                SecurityHeadersEnvVar.REFERRER_POLICY,
                SecurityHeadersConstants.REFERRER_POLICY,
            ),
            enable_hsts=EnvironmentParserUtility.parse_bool(
                SecurityHeadersEnvVar.ENABLE_HSTS,
                SecurityHeadersConstants.DEFAULT_ENABLE_HSTS,
            ),
            hsts_max_age=EnvironmentParserUtility.parse_int(
                SecurityHeadersEnvVar.HSTS_MAX_AGE,
                SecurityHeadersConstants.DEFAULT_HSTS_MAX_AGE_SECONDS,
            ),
            hsts_include_subdomains=EnvironmentParserUtility.parse_bool(
                SecurityHeadersEnvVar.HSTS_INCLUDE_SUBDOMAINS,
                SecurityHeadersConstants.DEFAULT_HSTS_INCLUDE_SUBDOMAINS,
            ),
            hsts_preload=EnvironmentParserUtility.parse_bool(
                SecurityHeadersEnvVar.HSTS_PRELOAD,
                SecurityHeadersConstants.DEFAULT_HSTS_PRELOAD,
            ),
            content_security_policy=csp,
            permissions_policy=EnvironmentParserUtility.parse_optional_str(
                SecurityHeadersEnvVar.PERMISSIONS_POLICY
            ),
            cross_origin_opener_policy=coop,
            cross_origin_resource_policy=corp,
            cross_origin_embedder_policy=EnvironmentParserUtility.parse_optional_str(
                SecurityHeadersEnvVar.CROSS_ORIGIN_EMBEDDER_POLICY
            ),
            remove_server_header=EnvironmentParserUtility.parse_bool(
                SecurityHeadersEnvVar.REMOVE_SERVER_HEADER,
                SecurityHeadersConstants.DEFAULT_REMOVE_SERVER_HEADER,
            ),
        )

    @classmethod
    def get_middleware_config(cls) -> SecurityHeadersConfig:
        """Return a :class:`SecurityHeadersConfig` for ``SecurityHeadersMiddleware``."""
        return cls.load_settings_from_env().to_middleware_config()


__all__ = ["SecurityHeadersUtility"]
