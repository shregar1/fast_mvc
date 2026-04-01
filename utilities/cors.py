"""CORS middleware configuration (env → DTO → ``CORSMiddleware`` keyword args)."""

from __future__ import annotations

import os
from typing import Any

from constants.cors import CorsDefaults
from dtos.configuration import CorsSettingsDTO
from utilities.env import EnvironmentParser


class CorsConfigUtil:
    """Utility class for CORS middleware configuration from environment variables."""

    @staticmethod
    def parse_allow_origins() -> list[str]:
        """Comma-separated origins; ``CORS_ORIGINS`` wins, else ``ALLOWED_ORIGINS`` (Docker)."""
        raw = os.getenv("CORS_ORIGINS") or os.getenv("ALLOWED_ORIGINS")
        if raw is None or str(raw).strip() == "":
            return ["*"]
        parts = [p.strip() for p in str(raw).split(",") if p.strip()]
        return parts if parts else ["*"]

    @staticmethod
    def parse_allow_headers() -> list[str]:
        """Parse CORS allow headers from environment."""
        raw = os.getenv("CORS_ALLOW_HEADERS")
        if raw is None or str(raw).strip() == "":
            return ["*"]
        s = str(raw).strip()
        if s == "*":
            return ["*"]
        return [p.strip() for p in s.split(",") if p.strip()]

    @classmethod
    def load_settings_from_env(cls) -> CorsSettingsDTO:
        """Load :class:`CorsSettingsDTO` from environment.

        Variables (all optional):

        - ``CORS_ORIGINS`` — comma-separated allowed origins; if unset, ``ALLOWED_ORIGINS``
          is used (Compose); if both empty, ``["*"]`` (permissive dev default).
        - ``CORS_ALLOW_CREDENTIALS`` — ``true`` / ``false`` (default ``true``).
        - ``CORS_ALLOW_METHODS`` — comma-separated verbs (default GET,POST,…).
        - ``CORS_ALLOW_HEADERS`` — ``*`` or comma-separated names (default ``*``).
        - ``CORS_EXPOSE_HEADERS`` — comma-separated (default includes transaction/reference URNs).
        - ``CORS_ALLOW_ORIGIN_REGEX`` — optional regex string.
        - ``CORS_MAX_AGE`` — preflight cache seconds (default ``600``).
        """
        allow_origin_regex = os.getenv("CORS_ALLOW_ORIGIN_REGEX")
        if allow_origin_regex is not None and allow_origin_regex.strip() == "":
            allow_origin_regex = None

        return CorsSettingsDTO(
            allow_origins=cls.parse_allow_origins(),
            allow_credentials=EnvironmentParser.parse_bool("CORS_ALLOW_CREDENTIALS", True),
            allow_methods=EnvironmentParser.parse_csv("CORS_ALLOW_METHODS", CorsDefaults.ALLOW_METHODS),
            allow_headers=cls.parse_allow_headers(),
            expose_headers=EnvironmentParser.parse_csv("CORS_EXPOSE_HEADERS", CorsDefaults.EXPOSE_HEADERS),
            allow_origin_regex=allow_origin_regex,
            max_age=EnvironmentParser.parse_int("CORS_MAX_AGE", 600),
        )

    @classmethod
    def get_middleware_kwargs(cls) -> dict[str, Any]:
        """Return keyword arguments for ``app.add_middleware(CORSMiddleware, **kwargs)``."""
        return cls.load_settings_from_env().to_middleware_kwargs()


__all__ = ["CorsConfigUtil"]
