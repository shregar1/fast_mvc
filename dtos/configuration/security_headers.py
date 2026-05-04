"""HTTP security headers configuration DTO."""

from __future__ import annotations

from typing import Final

from fastx_middleware import SecurityHeadersConfig  # pyright: ignore[reportMissingImports]
from pydantic import Field

from constants.security_headers import SecurityHeadersConstants, SecurityHeadersEnvVar
from dtos.configuration.abstraction import IConfigurationDTO


class SecurityHeadersDefaults:
    """Default values for :class:`SecurityHeadersSettingsDTO` fields.

    String defaults for standard headers align with :class:`~constants.security_headers.SecurityHeadersConstants`.
    ``CONTENT_SECURITY_POLICY`` is ``None`` on the model until
    :meth:`utilities.security_headers.SecurityHeadersUtility.load_settings_from_env` applies
    ``SecurityHeadersConstants.CONTENT_SECURITY_POLICY`` when
    :data:`~constants.security_headers.SecurityHeadersEnvVar.CONTENT_SECURITY_POLICY` is unset.
    """

    X_CONTENT_TYPE_OPTIONS: Final[str] = SecurityHeadersConstants.X_CONTENT_TYPE_OPTIONS
    X_FRAME_OPTIONS: Final[str] = SecurityHeadersConstants.X_FRAME_OPTIONS
    X_XSS_PROTECTION: Final[str] = SecurityHeadersConstants.X_XSS_PROTECTION
    REFERRER_POLICY: Final[str] = SecurityHeadersConstants.REFERRER_POLICY

    ENABLE_HSTS: Final[bool] = SecurityHeadersConstants.DEFAULT_ENABLE_HSTS
    HSTS_MAX_AGE: Final[int] = SecurityHeadersConstants.DEFAULT_HSTS_MAX_AGE_SECONDS
    HSTS_INCLUDE_SUBDOMAINS: Final[bool] = (
        SecurityHeadersConstants.DEFAULT_HSTS_INCLUDE_SUBDOMAINS
    )
    HSTS_PRELOAD: Final[bool] = SecurityHeadersConstants.DEFAULT_HSTS_PRELOAD

    CONTENT_SECURITY_POLICY: None = None
    PERMISSIONS_POLICY: None = None

    CROSS_ORIGIN_OPENER_POLICY: Final[str] = (
        SecurityHeadersConstants.CROSS_ORIGIN_OPENER_POLICY
    )
    CROSS_ORIGIN_RESOURCE_POLICY: Final[str] = (
        SecurityHeadersConstants.CROSS_ORIGIN_RESOURCE_POLICY
    )
    CROSS_ORIGIN_EMBEDDER_POLICY: None = None

    REMOVE_SERVER_HEADER: Final[bool] = SecurityHeadersConstants.DEFAULT_REMOVE_SERVER_HEADER

    BUILTIN_CONTENT_SECURITY_POLICY: Final[str] = (
        SecurityHeadersConstants.CONTENT_SECURITY_POLICY
    )
    """CSP applied at env load when :data:`~constants.security_headers.SecurityHeadersEnvVar.CONTENT_SECURITY_POLICY` is omitted."""


class SecurityHeadersSettingsDTO(IConfigurationDTO):
    """Typed settings for ``SecurityHeadersMiddleware`` (CSP, HSTS, frame options, …).

    Values are typically populated from environment variables; see
    :meth:`utilities.security_headers.SecurityHeadersUtility.load_settings_from_env`.
    """

    x_content_type_options: str = Field(
        default=SecurityHeadersDefaults.X_CONTENT_TYPE_OPTIONS,
        description="``X-Content-Type-Options`` (MIME sniffing).",
    )
    x_frame_options: str = Field(
        default=SecurityHeadersDefaults.X_FRAME_OPTIONS,
        description="``X-Frame-Options`` (e.g. DENY, SAMEORIGIN).",
    )
    x_xss_protection: str = Field(
        default=SecurityHeadersDefaults.X_XSS_PROTECTION,
        description="Legacy ``X-XSS-Protection`` value.",
    )
    referrer_policy: str = Field(
        default=SecurityHeadersDefaults.REFERRER_POLICY,
        description="``Referrer-Policy`` value.",
    )
    enable_hsts: bool = Field(
        default=SecurityHeadersDefaults.ENABLE_HSTS,
        description="Enable HTTP Strict Transport Security.",
    )
    hsts_max_age: int = Field(
        default=SecurityHeadersDefaults.HSTS_MAX_AGE,
        ge=0,
        description="HSTS ``max-age`` in seconds (default one year).",
    )
    hsts_include_subdomains: bool = Field(
        default=SecurityHeadersDefaults.HSTS_INCLUDE_SUBDOMAINS,
        description="Include ``includeSubDomains`` in HSTS.",
    )
    hsts_preload: bool = Field(
        default=SecurityHeadersDefaults.HSTS_PRELOAD,
        description="Enable HSTS preload list submission semantics.",
    )
    content_security_policy: str | None = Field(
        default=SecurityHeadersDefaults.CONTENT_SECURITY_POLICY,
        description=(
            "Full ``Content-Security-Policy`` header value. "
            "When omitted at load time, :class:`~constants.security_headers.SecurityHeadersConstants` is used."
        ),
    )
    permissions_policy: str | None = Field(
        default=SecurityHeadersDefaults.PERMISSIONS_POLICY,
        description="Optional ``Permissions-Policy`` header value.",
    )
    cross_origin_opener_policy: str = Field(
        default=SecurityHeadersDefaults.CROSS_ORIGIN_OPENER_POLICY,
        description="``Cross-Origin-Opener-Policy`` (COOP).",
    )
    cross_origin_resource_policy: str = Field(
        default=SecurityHeadersDefaults.CROSS_ORIGIN_RESOURCE_POLICY,
        description="``Cross-Origin-Resource-Policy`` (CORP).",
    )
    cross_origin_embedder_policy: str | None = Field(
        default=SecurityHeadersDefaults.CROSS_ORIGIN_EMBEDDER_POLICY,
        description="Optional ``Cross-Origin-Embedder-Policy`` (COEP).",
    )
    remove_server_header: bool = Field(
        default=SecurityHeadersDefaults.REMOVE_SERVER_HEADER,
        description="Strip the ``Server`` header from responses.",
    )

    def to_middleware_config(self) -> SecurityHeadersConfig:
        """Build the fastx-middleware :class:`~fastmiddleware.SecurityHeadersConfig` instance."""
        csp = self.content_security_policy
        return SecurityHeadersConfig(
            x_content_type_options=self.x_content_type_options,
            x_frame_options=self.x_frame_options,
            x_xss_protection=self.x_xss_protection,
            referrer_policy=self.referrer_policy,
            enable_hsts=self.enable_hsts,
            hsts_max_age=self.hsts_max_age,
            hsts_include_subdomains=self.hsts_include_subdomains,
            hsts_preload=self.hsts_preload,
            content_security_policy=csp,
            permissions_policy=self.permissions_policy,
            cross_origin_opener_policy=self.cross_origin_opener_policy,
            cross_origin_resource_policy=self.cross_origin_resource_policy,
            cross_origin_embedder_policy=self.cross_origin_embedder_policy,
            remove_server_header=self.remove_server_header,
        )
