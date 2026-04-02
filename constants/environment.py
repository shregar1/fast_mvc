"""Environment variable names for rate limiting (``RateLimitMiddleware`` / ``RateLimitConfig``)."""

from typing import Final


class EnvironmentVar:
    """Keys read by :mod:`app` and :mod:`start_utils` for per-client limits."""

    APP_NAME: Final[str] = "APP_NAME"
    APP_VERSION: Final[str] = "APP_VERSION"
    DEBUG: Final[str] = "DEBUG"
    LOG_LEVEL: Final[str] = "LOG_LEVEL"
    REQUESTS_PER_MINUTE: Final[str] = "RATE_LIMIT_REQUESTS_PER_MINUTE"
    REQUESTS_PER_HOUR: Final[str] = "RATE_LIMIT_REQUESTS_PER_HOUR"
    WINDOW_SECONDS: Final[str] = "RATE_LIMIT_WINDOW_SECONDS"
    BURST_LIMIT: Final[str] = "RATE_LIMIT_BURST_LIMIT"
    JWT_AUTH_ENABLED: Final[str] = "JWT_AUTH_ENABLED"
    IS_TEST_RUN: Final[str] = "PYTEST_CURRENT_TEST"
    VALIDATE_CONFIG: Final[str] = "VALIDATE_CONFIG"
    TESTING: Final[str] = "TESTING"
    TELEMETRY_ENABLED: Final[str] = "TELEMETRY_ENABLED"
    DATADOG_ENABLED: Final[str] = "DATADOG_ENABLED"
    HOST: Final[str] = "HOST"
    PORT: Final[str] = "PORT"
    SECRET_KEY: Final[str] = "SECRET_KEY"
    ALGORITHM: Final[str] = "ALGORITHM"
    ACCESS_TOKEN_EXPIRE_MINUTES: Final[str] = "ACCESS_TOKEN_EXPIRE_MINUTES"
    REFRESH_TOKEN_EXPIRE_DAYS: Final[str] = "REFRESH_TOKEN_EXPIRE_DAYS"
    FASTMVC_CONFIG_I: Final[str] = "FASTMVC_CONFIG_I"
    ACCESS_TOKEN_EXPIRE_MINUTE: Final[str] = "ACCESS_TOKEN_EXPIRE_MINUTE"
    CHANNEL_BACKEND: Final[str] = "CHANNEL_BACKEND"
