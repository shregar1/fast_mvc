"""Environment variable names aligned with ``.env.example``.

Use :class:`EnvironmentVar` for ``os.getenv`` / parsers so keys stay consistent
with the consolidated template and Docker Compose.
"""

from typing import Final


class EnvironmentVar:
    """String keys for environment variables (see ``.env.example``)."""

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    APP_NAME: Final[str] = "APP_NAME"
    APP_VERSION: Final[str] = "APP_VERSION"
    APP_ENV: Final[str] = "APP_ENV"
    DEBUG: Final[str] = "DEBUG"
    LOG_LEVEL: Final[str] = "LOG_LEVEL"
    LOG_FORMAT: Final[str] = "LOG_FORMAT"
    HOST: Final[str] = "HOST"
    PORT: Final[str] = "PORT"
    VALIDATE_CONFIG: Final[str] = "VALIDATE_CONFIG"

    # -------------------------------------------------------------------------
    # Security — JWT
    # -------------------------------------------------------------------------
    JWT_SECRET_KEY: Final[str] = "JWT_SECRET_KEY"
    SECRET_KEY: Final[str] = "SECRET_KEY"
    ALGORITHM: Final[str] = "ALGORITHM"
    JWT_AUTH_ENABLED: Final[str] = "JWT_AUTH_ENABLED"
    ACCESS_TOKEN_EXPIRE_MINUTE: Final[str] = "ACCESS_TOKEN_EXPIRE_MINUTE"
    # Legacy plural key (some deployments); prefer ``ACCESS_TOKEN_EXPIRE_MINUTE``.
    ACCESS_TOKEN_EXPIRE_MINUTES: Final[str] = "ACCESS_TOKEN_EXPIRE_MINUTES"
    REFRESH_TOKEN_EXPIRE_DAYS: Final[str] = "REFRESH_TOKEN_EXPIRE_DAYS"
    JWT_EXPIRATION_HOURS: Final[str] = "JWT_EXPIRATION_HOURS"
    BCRYPT_SALT: Final[str] = "BCRYPT_SALT"

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------
    DATABASE_URL: Final[str] = "DATABASE_URL"
    DATABASE_HOST: Final[str] = "DATABASE_HOST"
    DATABASE_PORT: Final[str] = "DATABASE_PORT"
    DATABASE_NAME: Final[str] = "DATABASE_NAME"
    DATABASE_USER: Final[str] = "DATABASE_USER"
    DATABASE_PASSWORD: Final[str] = "DATABASE_PASSWORD"
    DATABASE_POOL_SIZE: Final[str] = "DATABASE_POOL_SIZE"
    DATABASE_MAX_OVERFLOW: Final[str] = "DATABASE_MAX_OVERFLOW"

    # -------------------------------------------------------------------------
    # Redis
    # -------------------------------------------------------------------------
    REDIS_URL: Final[str] = "REDIS_URL"
    REDIS_HOST: Final[str] = "REDIS_HOST"
    REDIS_PORT: Final[str] = "REDIS_PORT"
    REDIS_PASSWORD: Final[str] = "REDIS_PASSWORD"
    REDIS_DB: Final[str] = "REDIS_DB"

    # -------------------------------------------------------------------------
    # CORS
    # -------------------------------------------------------------------------
    CORS_ORIGINS: Final[str] = "CORS_ORIGINS"
    ALLOWED_ORIGINS: Final[str] = "ALLOWED_ORIGINS"
    CORS_ALLOW_CREDENTIALS: Final[str] = "CORS_ALLOW_CREDENTIALS"
    CORS_ALLOW_METHODS: Final[str] = "CORS_ALLOW_METHODS"
    CORS_ALLOW_HEADERS: Final[str] = "CORS_ALLOW_HEADERS"

    # -------------------------------------------------------------------------
    # Rate limiting (``RateLimitMiddleware`` / ``RateLimitConfig``)
    # -------------------------------------------------------------------------
    RATE_LIMIT_REQUESTS_PER_MINUTE: Final[str] = "RATE_LIMIT_REQUESTS_PER_MINUTE"
    RATE_LIMIT_REQUESTS_PER_HOUR: Final[str] = "RATE_LIMIT_REQUESTS_PER_HOUR"
    RATE_LIMIT_WINDOW_SECONDS: Final[str] = "RATE_LIMIT_WINDOW_SECONDS"
    RATE_LIMIT_BURST_LIMIT: Final[str] = "RATE_LIMIT_BURST_LIMIT"
    # Short names used by ``app.py`` middleware wiring
    REQUESTS_PER_MINUTE: Final[str] = "RATE_LIMIT_REQUESTS_PER_MINUTE"
    REQUESTS_PER_HOUR: Final[str] = "RATE_LIMIT_REQUESTS_PER_HOUR"
    WINDOW_SECONDS: Final[str] = "RATE_LIMIT_WINDOW_SECONDS"
    BURST_LIMIT: Final[str] = "RATE_LIMIT_BURST_LIMIT"

    # -------------------------------------------------------------------------
    # API documentation (HTTP Basic for /docs, /redoc)
    # -------------------------------------------------------------------------
    DOCS_USERNAME: Final[str] = "DOCS_USERNAME"
    DOCS_PASSWORD: Final[str] = "DOCS_PASSWORD"
    OPENAPI_URL: Final[str] = "OPENAPI_URL"
    DOCS_EXTRA_PROTECTED_PATHS: Final[str] = "DOCS_EXTRA_PROTECTED_PATHS"

    # -------------------------------------------------------------------------
    # Postman export
    # -------------------------------------------------------------------------
    POSTMAN_OUTPUT_DIR: Final[str] = "POSTMAN_OUTPUT_DIR"
    POSTMAN_COLLECTION_FILE: Final[str] = "POSTMAN_COLLECTION_FILE"
    POSTMAN_EXPORT_ENVIRONMENT: Final[str] = "POSTMAN_EXPORT_ENVIRONMENT"
    POSTMAN_ENV_FILE: Final[str] = "POSTMAN_ENV_FILE"
    POSTMAN_COLLECTION_NAME: Final[str] = "POSTMAN_COLLECTION_NAME"
    POSTMAN_BASE_URL: Final[str] = "POSTMAN_BASE_URL"
    POSTMAN_NEGATIVE_TESTS: Final[str] = "POSTMAN_NEGATIVE_TESTS"

    # -------------------------------------------------------------------------
    # Telemetry
    # -------------------------------------------------------------------------
    TELEMETRY_ENABLED: Final[str] = "TELEMETRY_ENABLED"
    DATADOG_ENABLED: Final[str] = "DATADOG_ENABLED"

    # -------------------------------------------------------------------------
    # Docker Compose (infrastructure)
    # -------------------------------------------------------------------------
    POSTGRES_USER: Final[str] = "POSTGRES_USER"
    POSTGRES_PASSWORD: Final[str] = "POSTGRES_PASSWORD"
    POSTGRES_DB: Final[str] = "POSTGRES_DB"
    POSTGRES_PORT: Final[str] = "POSTGRES_PORT"
    PGADMIN_EMAIL: Final[str] = "PGADMIN_EMAIL"
    PGADMIN_PASSWORD: Final[str] = "PGADMIN_PASSWORD"
    PGADMIN_PORT: Final[str] = "PGADMIN_PORT"
    REDIS_INSIGHT_PORT: Final[str] = "REDIS_INSIGHT_PORT"
    NGINX_HTTP_PORT: Final[str] = "NGINX_HTTP_PORT"
    NGINX_HTTPS_PORT: Final[str] = "NGINX_HTTPS_PORT"

    # -------------------------------------------------------------------------
    # Optional: LLM providers
    # -------------------------------------------------------------------------
    OPENAI_ENABLED: Final[str] = "OPENAI_ENABLED"
    OPENAI_API_KEY: Final[str] = "OPENAI_API_KEY"
    OPENAI_BASE_URL: Final[str] = "OPENAI_BASE_URL"
    OPENAI_MODEL: Final[str] = "OPENAI_MODEL"
    ANTHROPIC_ENABLED: Final[str] = "ANTHROPIC_ENABLED"
    ANTHROPIC_API_KEY: Final[str] = "ANTHROPIC_API_KEY"
    ANTHROPIC_BASE_URL: Final[str] = "ANTHROPIC_BASE_URL"
    ANTHROPIC_MODEL: Final[str] = "ANTHROPIC_MODEL"
    OLLAMA_ENABLED: Final[str] = "OLLAMA_ENABLED"
    OLLAMA_BASE_URL: Final[str] = "OLLAMA_BASE_URL"
    OLLAMA_MODEL: Final[str] = "OLLAMA_MODEL"
    GEMINI_ENABLED: Final[str] = "GEMINI_ENABLED"
    GEMINI_API_KEY: Final[str] = "GEMINI_API_KEY"
    GEMINI_MODEL: Final[str] = "GEMINI_MODEL"

    # -------------------------------------------------------------------------
    # Optional: push notifications
    # -------------------------------------------------------------------------
    APNS_ENABLED: Final[str] = "APNS_ENABLED"
    APNS_KEY_ID: Final[str] = "APNS_KEY_ID"
    APNS_TEAM_ID: Final[str] = "APNS_TEAM_ID"
    APNS_BUNDLE_ID: Final[str] = "APNS_BUNDLE_ID"
    APNS_PRIVATE_KEY_PATH: Final[str] = "APNS_PRIVATE_KEY_PATH"
    APNS_USE_SANDBOX: Final[str] = "APNS_USE_SANDBOX"
    FCM_ENABLED: Final[str] = "FCM_ENABLED"
    FCM_SERVER_KEY: Final[str] = "FCM_SERVER_KEY"
    FCM_PROJECT_ID: Final[str] = "FCM_PROJECT_ID"

    # -------------------------------------------------------------------------
    # Development (uvicorn)
    # -------------------------------------------------------------------------
    RELOAD: Final[str] = "RELOAD"
    WORKERS: Final[str] = "WORKERS"

    # -------------------------------------------------------------------------
    # Runtime / testing / project
    # -------------------------------------------------------------------------
    IS_TEST_RUN: Final[str] = "PYTEST_CURRENT_TEST"
    TESTING: Final[str] = "TESTING"
    FASTMVC_CONFIG_I: Final[str] = "FASTMVC_CONFIG_I"
    CHANNEL_BACKEND: Final[str] = "CHANNEL_BACKEND"
