"""Default CORS middleware lists (aligned with :class:`dtos.configuration.CorsSettingsDTO`)."""

from typing import ClassVar, Final

from constants.http_header import HttpHeader
from constants.http_method import HttpMethod


class CorsEnvVar:
    """Environment variable names for :mod:`utilities.cors` / ``CORSMiddleware``."""

    ORIGINS: Final[str] = "CORS_ORIGINS"
    ALLOWED_ORIGINS: Final[str] = "ALLOWED_ORIGINS"
    ALLOW_CREDENTIALS: Final[str] = "CORS_ALLOW_CREDENTIALS"
    ALLOW_METHODS: Final[str] = "CORS_ALLOW_METHODS"
    ALLOW_HEADERS: Final[str] = "CORS_ALLOW_HEADERS"
    EXPOSE_HEADERS: Final[str] = "CORS_EXPOSE_HEADERS"
    ALLOW_ORIGIN_REGEX: Final[str] = "CORS_ALLOW_ORIGIN_REGEX"
    MAX_AGE: Final[str] = "CORS_MAX_AGE"


class CorsDefaults:
    """Default CORS allow-methods, wildcards, and env fallbacks (overridden in :mod:`utilities.cors`)."""

    WILDCARD: Final[str] = "*"
    """Origin / header sentinel when the env leaves lists unspecified (dev-permissive)."""

    FALLBACK_ALLOW_ORIGINS: ClassVar[tuple[str, ...]] = (WILDCARD,)
    """Used when :data:`CorsEnvVar.ORIGINS` / :data:`CorsEnvVar.ALLOWED_ORIGINS` are unset or empty."""

    FALLBACK_ALLOW_HEADERS: ClassVar[tuple[str, ...]] = (WILDCARD,)
    """Used when :data:`CorsEnvVar.ALLOW_HEADERS` is unset, empty, or exactly :data:`WILDCARD`."""

    DEFAULT_ALLOW_CREDENTIALS: Final[bool] = True
    """Default for :data:`CorsEnvVar.ALLOW_CREDENTIALS` when the env var is omitted."""

    DEFAULT_MAX_AGE_SECONDS: Final[int] = 600
    """Default ``Access-Control-Max-Age`` (preflight cache) when :data:`CorsEnvVar.MAX_AGE` is omitted."""

    ALLOW_METHODS: ClassVar[tuple[str, ...]] = (
        HttpMethod.GET,
        HttpMethod.POST,
        HttpMethod.PUT,
        HttpMethod.DELETE,
        HttpMethod.OPTIONS,
        HttpMethod.PATCH,
    )
    EXPOSE_HEADERS: ClassVar[tuple[str, ...]] = (
        HttpHeader.X_REQUEST_ID,
        HttpHeader.X_PROCESS_TIME,
        HttpHeader.X_TRANSACTION_URN,
        HttpHeader.X_REFERENCE_URN,
    )

    CORS_DEFAULT_ALLOW_METHODS: Final[tuple[str, ...]] = ALLOW_METHODS
    CORS_DEFAULT_EXPOSE_HEADERS: Final[tuple[str, ...]] = EXPOSE_HEADERS
