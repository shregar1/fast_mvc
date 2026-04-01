"""CORS middleware configuration (env → DTO → ``CORSMiddleware`` keyword args)."""

from __future__ import annotations

import os
from typing import Any, Optional

from abstractions.utility import IUtility
from constants.cors import CorsDefaults, CorsEnvVar
from dtos.configuration import CorsSettingsDTO
from utilities.env import EnvironmentParserUtility


class CorsConfigUtility(IUtility):
    """Utility class for CORS middleware configuration from environment variables."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> None:
        """Initialize the CORS config utility.

        Args:
            urn: Unique Request Number for tracing.
            user_urn: User's unique resource name.
            api_name: Name of the API endpoint.
            user_id: Database identifier of the user.
        """
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
        )

    @staticmethod
    def parse_allow_origins() -> list[str]:
        """Comma-separated origins; :data:`CorsEnvVar.ORIGINS` wins, else :data:`CorsEnvVar.ALLOWED_ORIGINS` (Docker)."""
        raw = os.getenv(CorsEnvVar.ORIGINS) or os.getenv(CorsEnvVar.ALLOWED_ORIGINS)
        if raw is None or str(raw).strip() == "":
            return list(CorsDefaults.FALLBACK_ALLOW_ORIGINS)
        parts = [p.strip() for p in str(raw).split(",") if p.strip()]
        return parts if parts else list(CorsDefaults.FALLBACK_ALLOW_ORIGINS)

    @staticmethod
    def parse_allow_headers() -> list[str]:
        """Parse CORS allow headers from :data:`CorsEnvVar.ALLOW_HEADERS`."""
        raw = os.getenv(CorsEnvVar.ALLOW_HEADERS)
        if raw is None or str(raw).strip() == "":
            return list(CorsDefaults.FALLBACK_ALLOW_HEADERS)
        s = str(raw).strip()
        if s == CorsDefaults.WILDCARD:
            return list(CorsDefaults.FALLBACK_ALLOW_HEADERS)
        return [p.strip() for p in s.split(",") if p.strip()]

    @classmethod
    def load_settings_from_env(cls) -> CorsSettingsDTO:
        """Load :class:`CorsSettingsDTO` from environment.

        Defaults match :class:`constants.cors.CorsDefaults` (wildcard, methods, credentials,
        max-age, expose-headers).

        Variables (all optional):

        - :data:`CorsEnvVar.ORIGINS` — comma-separated allowed origins; if unset,
          :data:`CorsEnvVar.ALLOWED_ORIGINS` is used (Compose); if both empty,
          :data:`CorsDefaults.FALLBACK_ALLOW_ORIGINS`.
        - :data:`CorsEnvVar.ALLOW_CREDENTIALS` — ``true`` / ``false`` (default
          :data:`CorsDefaults.DEFAULT_ALLOW_CREDENTIALS`).
        - :data:`CorsEnvVar.ALLOW_METHODS` — comma-separated verbs (default
          :data:`CorsDefaults.ALLOW_METHODS`).
        - :data:`CorsEnvVar.ALLOW_HEADERS` — :data:`CorsDefaults.WILDCARD` or comma-separated names
          (default :data:`CorsDefaults.FALLBACK_ALLOW_HEADERS`).
        - :data:`CorsEnvVar.EXPOSE_HEADERS` — comma-separated (default
          :data:`CorsDefaults.EXPOSE_HEADERS`).
        - :data:`CorsEnvVar.ALLOW_ORIGIN_REGEX` — optional regex string.
        - :data:`CorsEnvVar.MAX_AGE` — preflight cache seconds (default
          :data:`CorsDefaults.DEFAULT_MAX_AGE_SECONDS`).
        """
        allow_origin_regex = os.getenv(CorsEnvVar.ALLOW_ORIGIN_REGEX)
        if allow_origin_regex is not None and allow_origin_regex.strip() == "":
            allow_origin_regex = None

        return CorsSettingsDTO(
            allow_origins=cls.parse_allow_origins(),
            allow_credentials=EnvironmentParserUtility.parse_bool(
                CorsEnvVar.ALLOW_CREDENTIALS, CorsDefaults.DEFAULT_ALLOW_CREDENTIALS
            ),
            allow_methods=EnvironmentParserUtility.parse_csv(
                CorsEnvVar.ALLOW_METHODS, CorsDefaults.ALLOW_METHODS
            ),
            allow_headers=cls.parse_allow_headers(),
            expose_headers=EnvironmentParserUtility.parse_csv(
                CorsEnvVar.EXPOSE_HEADERS, CorsDefaults.EXPOSE_HEADERS
            ),
            allow_origin_regex=allow_origin_regex,
            max_age=EnvironmentParserUtility.parse_int(
                CorsEnvVar.MAX_AGE, CorsDefaults.DEFAULT_MAX_AGE_SECONDS
            ),
        )

    @classmethod
    def get_middleware_kwargs(cls) -> dict[str, Any]:
        """Return keyword arguments for ``app.add_middleware(CORSMiddleware, **kwargs)``."""
        return cls.load_settings_from_env().to_middleware_kwargs()


__all__ = ["CorsConfigUtility"]
