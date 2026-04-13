"""Default Configuration Constants Module.

This module defines default values for application configuration settings.
These defaults are used as fallbacks when configuration files are missing
or when specific values are not provided.

Domain-specific defaults live on :class:`ApplicationDefault`, :class:`JwtDefault`,
:class:`RateLimitDefault`, etc. :class:`Default` inherits all of them and adds
:data:`Default.SECURITY_CONFIGURATION`.

Usage:
    >>> from constants.default import Default
    >>> token_expiry = config.get("expiry", Default.ACCESS_TOKEN_EXPIRE_MINUTES)
"""

from typing import Any, Final

from constants.cors import CorsDefaults
from constants.http_method import HttpMethod
from constants.security_headers import SecurityHeadersConstants

__all__ = [
    "ApplicationDefault",
    "AuthenticationDefault",
    "CorsSectionDefault",
    "Default",
    "InputValidationDefault",
    "JwtDefault",
    "PostmanDefault",
    "RateLimitDefault",
    "RateLimitingDefault",
    "SecurityHeadersDefault",
    "TimeoutDefault",
]


class ApplicationDefault:
    """Core app identity, logging, and channel settings."""

    APP_NAME: Final[str] = "FastX"
    """Default application name."""

    APP_VERSION: Final[str] = "1.0.1"
    """Default application version."""

    DEBUG: Final[bool] = False
    """Default debug mode."""

    LOG_LEVEL: Final[str] = "INFO"
    """Default log level."""

    CHANNEL_BACKEND: Final[str] = "redis"
    """Default channels backend."""

    ALLOW_ORIGIN_REGEX: Final[str] = ""
    """Default allow origin regex."""

    GRPC_ENABLED: Final[bool] = False
    """Enable optional gRPC server transport (developer opt-in)."""

    GRPC_HOST: Final[str] = "0.0.0.0"
    """gRPC listen host when `GRPC_ENABLED=true`."""

    GRPC_PORT: Final[int] = 50051
    """gRPC listen port when `GRPC_ENABLED=true`."""

    HOST: Final[str] = "0.0.0.0"
    PORT: Final[int] = 8000
    REDIS_HOST: Final[str] = "localhost"
    REDIS_PORT: Final[int] = 6379
    ENCODING_UTF8: Final[str] = "utf-8"
    BOOLEAN_TRUE_VALUES: Final[tuple[str, ...]] = ("true", "1", "yes", "on")
    BOOLEAN_FALSE_VALUES: Final[tuple[str, ...]] = ("false", "0", "no", "off")
    VALID_ENVIRONMENTS: Final[tuple[str, ...]] = (
        "development",
        "dev",
        "staging",
        "stage",
        "production",
        "prod",
        "test",
        "testing",
    )
    DATABASE_URL_SQLITE: Final[str] = "sqlite:///./app.db"


class JwtDefault:
    """JWT signing and token lifetime defaults."""

    ALGORITHM: Final[str] = "HS256"
    """Default JWT algorithm."""

    JWT_AUTH_ENABLED: Final[bool] = False
    """Default JWT authentication enabled."""

    SECRET_KEY: Final[str] = ""
    """Default JWT secret key."""

    ACCESS_TOKEN_EXPIRE_MINUTE: Final[int] = 1440
    """Default JWT access token expiry: 24 hours (1440 minutes)."""

    ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = ACCESS_TOKEN_EXPIRE_MINUTE
    """Alias of :data:`ACCESS_TOKEN_EXPIRE_MINUTE` (plural name used in docs and examples)."""

    REFRESH_TOKEN_EXPIRE_DAYS: Final[int] = 7
    """Default JWT refresh token expiry: 7 days."""

    ACCESS_TOKEN_EXPIRE_MINUTES_SHORT: Final[int] = 30
    """Short-lived access token expiry in minutes."""


class RateLimitDefault:
    """Numeric limits used by middleware and ``RATE_LIMITING_CONFIGURATION``."""

    RATE_LIMIT_MAX_REQUESTS: Final[int] = 2
    """Maximum requests per rate limit window."""

    RATE_LIMIT_WINDOW_SECONDS: Final[int] = 60
    """Rate limit window duration in seconds."""

    RATE_LIMIT_REQUESTS_PER_MINUTE: Final[int] = 60
    """Allowed requests per minute per client."""

    RATE_LIMIT_REQUESTS_PER_HOUR: Final[int] = 1000
    """Allowed requests per hour per client."""

    RATE_LIMIT_BURST_LIMIT: Final[int] = 10
    """Maximum burst requests allowed."""


class AuthenticationDefault:
    """Security-config authentication subsection scalars and nested dict."""

    SECURITY_JWT_EXPIRY_MINUTES: Final[int] = 30
    """JWT expiry in minutes for ``SECURITY_CONFIGURATION`` authentication (nested default)."""

    MAX_LOGIN_ATTEMPTS: Final[int] = 5
    """Failed attempts before lockout (``SECURITY_CONFIGURATION`` authentication)."""

    LOCKOUT_DURATION_MINUTES: Final[int] = 15
    """Account lockout duration in minutes."""

    PASSWORD_HISTORY_COUNT: Final[int] = 5
    """Passwords remembered for reuse checks."""

    REQUIRE_STRONG_PASSWORD: Final[bool] = True
    """Require strong password policy in security config defaults."""

    SESSION_TIMEOUT_MINUTES: Final[int] = 60
    """Idle session timeout in minutes."""

    EMAIL_TOKEN_EXPIRY_MINUTES: Final[int] = 60
    """Email token expiry in minutes."""

    MFA_TOKEN_EXPIRY_MINUTES: Final[int] = 10
    """MFA token expiry in minutes."""

    MFA_TIME_STEP_SECONDS: Final[int] = 30
    """MFA TOTP time step in seconds."""

    AUTHENTICATION_REQUIRED_MESSAGE: Final[str] = "Authentication required"
    """Default authentication required message."""

    AUTHENTICATION_CONFIGURATION: Final[dict[str, Any]] = {
        "jwt_expiry_minutes": SECURITY_JWT_EXPIRY_MINUTES,
        "refresh_token_expiry_days": JwtDefault.REFRESH_TOKEN_EXPIRE_DAYS,
        "max_login_attempts": MAX_LOGIN_ATTEMPTS,
        "lockout_duration_minutes": LOCKOUT_DURATION_MINUTES,
        "password_history_count": PASSWORD_HISTORY_COUNT,
        "require_strong_password": REQUIRE_STRONG_PASSWORD,
        "session_timeout_minutes": SESSION_TIMEOUT_MINUTES,
    }
    # Defaults for ``SECURITY_CONFIGURATION["authentication"]``.


class PostmanDefault:
    """Postman collection generation defaults."""

    SCRIPT_TYPE_JAVASCRIPT: Final[str] = "text/javascript"
    """Postman script type for JavaScript."""


class TimeoutDefault:
    """Timeout defaults for various operations."""

    DEFAULT_TIMEOUT_SECONDS: Final[int] = 30
    """Default timeout in seconds for async operations."""


class RateLimitingDefault:
    """Flags, paths, and nested ``rate_limiting`` security-config dict."""

    RATE_LIMITING_ENABLE_SLIDING_WINDOW: Final[bool] = True
    RATE_LIMITING_ENABLE_TOKEN_BUCKET: Final[bool] = False
    RATE_LIMITING_ENABLE_FIXED_WINDOW: Final[bool] = False
    RATE_LIMITING_EXCLUDED_PATHS: Final[tuple[str, ...]] = (
        "/health",
        "/docs",
        "/openapi.json",
    )
    RATE_LIMITING_EXCLUDED_METHODS: Final[tuple[str, ...]] = ("OPTIONS",)

    RATE_LIMITING_CONFIGURATION: Final[dict[str, Any]] = {
        "requests_per_minute": RateLimitDefault.RATE_LIMIT_REQUESTS_PER_MINUTE,
        "requests_per_hour": RateLimitDefault.RATE_LIMIT_REQUESTS_PER_HOUR,
        "burst_limit": RateLimitDefault.RATE_LIMIT_BURST_LIMIT,
        "window_size": RateLimitDefault.RATE_LIMIT_WINDOW_SECONDS,
        "enable_sliding_window": RATE_LIMITING_ENABLE_SLIDING_WINDOW,
        "enable_token_bucket": RATE_LIMITING_ENABLE_TOKEN_BUCKET,
        "enable_fixed_window": RATE_LIMITING_ENABLE_FIXED_WINDOW,
        "excluded_paths": list(RATE_LIMITING_EXCLUDED_PATHS),
        "excluded_methods": list(RATE_LIMITING_EXCLUDED_METHODS),
    }
    # Defaults for ``SECURITY_CONFIGURATION["rate_limiting"]``.


class SecurityHeadersDefault:
    """HTTP security header policy defaults for ``SECURITY_CONFIGURATION``."""

    SECURITY_HEADERS_ENABLE_HSTS: Final[bool] = True
    SECURITY_HEADERS_ENABLE_CSP: Final[bool] = True
    SECURITY_HEADERS_CSP_REPORT_ONLY: Final[bool] = False
    SECURITY_HEADERS_HSTS_MAX_AGE: Final[int] = 31_536_000
    SECURITY_HEADERS_HSTS_INCLUDE_SUBDOMAINS: Final[bool] = True
    SECURITY_HEADERS_HSTS_PRELOAD: Final[bool] = False

    SECURITY_HEADERS_CONFIGURATION: Final[dict[str, Any]] = {
        "enable_hsts": SECURITY_HEADERS_ENABLE_HSTS,
        "enable_csp": SECURITY_HEADERS_ENABLE_CSP,
        "csp_report_only": SECURITY_HEADERS_CSP_REPORT_ONLY,
        "hsts_max_age": SECURITY_HEADERS_HSTS_MAX_AGE,
        "hsts_include_subdomains": SECURITY_HEADERS_HSTS_INCLUDE_SUBDOMAINS,
        "hsts_preload": SECURITY_HEADERS_HSTS_PRELOAD,
        "frame_options": SecurityHeadersConstants.X_FRAME_OPTIONS,
        "content_type_options": SecurityHeadersConstants.X_CONTENT_TYPE_OPTIONS,
        "xss_protection": SecurityHeadersConstants.X_XSS_PROTECTION,
        "referrer_policy": SecurityHeadersConstants.REFERRER_POLICY,
        "custom_csp": None,
        "custom_permissions_policy": None,
    }
    # Defaults for ``SECURITY_CONFIGURATION["security_headers"]``.


class InputValidationDefault:
    """Input validation limits and ``input_validation`` security-config dict."""

    INPUT_VALIDATION_MAX_STRING_LENGTH: Final[int] = 1000
    """Default max general string length (``SECURITY_CONFIGURATION`` input_validation)."""

    INPUT_VALIDATION_MAX_PASSWORD_LENGTH: Final[int] = 128
    """Default max password length."""

    INPUT_VALIDATION_MIN_PASSWORD_LENGTH: Final[int] = 8
    """Default min password length."""

    INPUT_VALIDATION_MAX_EMAIL_LENGTH: Final[int] = 254
    """Default max email length (RFC-friendly upper bound)."""

    INPUT_VALIDATION_ENABLE_SQL_INJECTION_CHECK: Final[bool] = True
    INPUT_VALIDATION_ENABLE_XSS_CHECK: Final[bool] = True
    INPUT_VALIDATION_ENABLE_PATH_TRAVERSAL_CHECK: Final[bool] = True
    INPUT_VALIDATION_WEAK_PASSWORDS: Final[tuple[str, ...]] = (
        "password",
        "123456",
        "qwerty",
        "admin",
        "letmein",
    )

    INPUT_VALIDATION_CONFIGURATION: Final[dict[str, Any]] = {
        "max_string_length": INPUT_VALIDATION_MAX_STRING_LENGTH,
        "max_password_length": INPUT_VALIDATION_MAX_PASSWORD_LENGTH,
        "min_password_length": INPUT_VALIDATION_MIN_PASSWORD_LENGTH,
        "max_email_length": INPUT_VALIDATION_MAX_EMAIL_LENGTH,
        "enable_sql_injection_check": INPUT_VALIDATION_ENABLE_SQL_INJECTION_CHECK,
        "enable_xss_check": INPUT_VALIDATION_ENABLE_XSS_CHECK,
        "enable_path_traversal_check": INPUT_VALIDATION_ENABLE_PATH_TRAVERSAL_CHECK,
        "weak_passwords": list(INPUT_VALIDATION_WEAK_PASSWORDS),
    }
    # Defaults for ``SECURITY_CONFIGURATION["input_validation"]`` (see scalars above).


class CorsSectionDefault:
    """CORS tuples and ``cors`` subsection of ``SECURITY_CONFIGURATION``."""

    CORS_DEFAULT_ALLOWED_ORIGINS: Final[tuple[str, ...]] = (CorsDefaults.WILDCARD,)
    CORS_DEFAULT_ALLOWED_METHODS: Final[tuple[str, ...]] = (
        HttpMethod.GET,
        HttpMethod.POST,
        HttpMethod.PUT,
        HttpMethod.DELETE,
        HttpMethod.OPTIONS,
    )
    CORS_DEFAULT_ALLOWED_HEADERS: Final[tuple[str, ...]] = (CorsDefaults.WILDCARD,)
    CORS_DEFAULT_ALLOW_CREDENTIALS: Final[bool] = True
    CORS_DEFAULT_MAX_AGE: Final[int] = 3600

    CORS_CONFIGURATION: Final[dict[str, Any]] = {
        "allowed_origins": list(CORS_DEFAULT_ALLOWED_ORIGINS),
        "allowed_methods": list(CORS_DEFAULT_ALLOWED_METHODS),
        "allowed_headers": list(CORS_DEFAULT_ALLOWED_HEADERS),
        "allow_credentials": CORS_DEFAULT_ALLOW_CREDENTIALS,
        "max_age": CORS_DEFAULT_MAX_AGE,
    }
    # Defaults for ``SECURITY_CONFIGURATION["cors"]`` (see tuples/bools above).


class Default(
    ApplicationDefault,
    JwtDefault,
    RateLimitDefault,
    AuthenticationDefault,
    RateLimitingDefault,
    SecurityHeadersDefault,
    InputValidationDefault,
    CorsSectionDefault,
    TimeoutDefault,
):
    """Aggregated defaults for FastX (inherits domain classes above).

    Use :data:`SECURITY_CONFIGURATION` for the combined security nested dict;
    subsection dicts are also exposed on the same names as the domain classes
    (e.g. :data:`AuthenticationDefault.AUTHENTICATION_CONFIGURATION` and
    :data:`Default.AUTHENTICATION_CONFIGURATION` are identical via inheritance).

    Note:
        These defaults are designed for development. Production deployments
        should use explicit configuration files with stricter values.

    Security configuration structure:
        - rate_limiting: Request rate limiting settings
        - security_headers: HTTP security header configuration
        - input_validation: Input sanitization and validation rules
        - authentication: JWT and session settings
        - cors: Cross-Origin Resource Sharing settings
    """

    SECURITY_CONFIGURATION: Final[dict[str, Any]] = {
        "rate_limiting": RateLimitingDefault.RATE_LIMITING_CONFIGURATION,
        "security_headers": SecurityHeadersDefault.SECURITY_HEADERS_CONFIGURATION,
        "input_validation": InputValidationDefault.INPUT_VALIDATION_CONFIGURATION,
        "authentication": AuthenticationDefault.AUTHENTICATION_CONFIGURATION,
        "cors": CorsSectionDefault.CORS_CONFIGURATION,
    }
