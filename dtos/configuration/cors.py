"""CORS configuration DTO."""

from __future__ import annotations

import inspect
from typing import Any

from fastmiddleware import CORSMiddleware  # pyright: ignore[reportMissingImports]
from pydantic import Field

from constants.cors import CorsDefaults
from dtos.configuration.abstraction import IConfigurationDTO


class CorsSettingsDTO(IConfigurationDTO):
    """Typed settings for ``CORSMiddleware`` (cross-origin resource sharing).

    Loaded from environment in :mod:`utilities.cors` and applied via
    :meth:`to_middleware_kwargs` in ``app.py``.
    """

    allow_origins: list[str] = Field(
        default_factory=lambda: list(CorsDefaults.FALLBACK_ALLOW_ORIGINS),
        description="Allowed ``Origin`` values (use ``*`` only for development).",
    )
    allow_credentials: bool = Field(
        default=CorsDefaults.DEFAULT_ALLOW_CREDENTIALS,
        description="Whether cookies/auth may be sent cross-origin.",
    )
    allow_methods: list[str] = Field(
        default_factory=lambda: list(CorsDefaults.ALLOW_METHODS),
        description="HTTP methods permitted in CORS.",
    )
    allow_headers: list[str] = Field(
        default_factory=lambda: list(CorsDefaults.FALLBACK_ALLOW_HEADERS),
        description="Request headers browsers may send (``*`` = any).",
    )
    expose_headers: list[str] = Field(
        default_factory=lambda: list(CorsDefaults.EXPOSE_HEADERS),
        description="Response headers exposed to browser JavaScript.",
    )
    allow_origin_regex: str = Field(
        default=None,
        description="Optional regex matched against ``Origin`` (e.g. ``https://.*\\.example\\.com``).",
    )
    max_age: int = Field(
        default=CorsDefaults.DEFAULT_MAX_AGE_SECONDS,
        ge=0,
        description="``Access-Control-Max-Age`` for preflight cache (seconds).",
    )

    def to_middleware_kwargs(self) -> dict[str, Any]:
        """Keyword arguments for ``app.add_middleware(CORSMiddleware, **kwargs)``.

        Only parameters supported by the installed ``fastmiddleware.CORSMiddleware``
        are returned (signature may differ from Starlette’s built-in CORS middleware).
        """
        raw: dict[str, Any] = {
            "allow_origins": list(self.allow_origins),
            "allow_credentials": self.allow_credentials,
            "allow_methods": list(self.allow_methods),
            "allow_headers": list(self.allow_headers),
            "expose_headers": list(self.expose_headers),
            "max_age": self.max_age,
        }
        if self.allow_origin_regex:
            raw["allow_origin_regex"] = self.allow_origin_regex
        supported = set(inspect.signature(CORSMiddleware.__init__).parameters) - {
            "self",
            "app",
        }
        return {k: v for k, v in raw.items() if k in supported}
