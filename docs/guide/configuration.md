# Configuration

FastMVC uses environment variables for configuration with built-in validation.

## Environment Variables

Create a `.env` file in your project root:

```bash
# Application
APP_NAME=My FastMVC App
APP_VERSION=1.0.0
DEBUG=false

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# HTTP security headers (optional — see Security headers section)
# SECURITY_ENABLE_HSTS=true
# SECURITY_CONTENT_SECURITY_POLICY=default-src 'self'; ...

# Server
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# DataI (optional)
DATABASE_URL=sqlite:///./app.db
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# CORS (see CORS section — prefer CORS_* variables)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
# CORS_ORIGINS=http://localhost:3000,http://localhost:8080
# CORS_ALLOW_CREDENTIALS=true
# CORS_EXPOSE_HEADERS=X-Request-ID,X-Process-Time,x-transaction-urn,x-reference-urn

# API documentation (Swagger / ReDoc / OpenAPI) — optional HTTP Basic auth
# DOCS_USERNAME=... 
# DOCS_PASSWORD=...
# OPENAPI_URL=/openapi.json
# DOCS_EXTRA_PROTECTED_PATHS=
```

See [API Documentation](api-docs.md) for how documentation routes are protected, which paths are covered, and nginx notes.

## Configuration Validation

FastMVC validates configuration on startup and fails fast with clear error messages.

### JWT Secret Validation

The `SECRET_KEY` must:

- Be at least 32 characters long
- Not be a common weak value (like "secret", "password", etc.)

### DataI URL Validation

Supported database schemes:

- `sqlite`
- `postgresql` / `postgres`
- `mysql` / `mysql+aiomysql`
- `redis`

### Skip Validation

To skip validation (e.g., for testing):

```bash
VALIDATE_CONFIG=false python app.py
```

Or in `.env`:

```bash
VALIDATE_CONFIG=false
```

## CORS

`CORSMiddleware` (from `fastmiddleware`, Starlette-compatible) is configured via `dtos.configuration.CorsSettingsDTO` (inherits `IConfigurationDTO`), loaded by `utilities.cors.CorsConfigUtility.load_settings_from_env()` and applied in `app.py` with `CorsConfigUtility.get_middleware_kwargs()`.

| Variable | Purpose |
|----------|---------|
| `CorsEnvVar.ORIGINS` | Comma-separated allowed `Origin` values. If unset, `CorsEnvVar.ALLOWED_ORIGINS` is used (e.g. Docker Compose). If both are empty, defaults to `CorsDefaults.FALLBACK_ALLOW_ORIGINS` (wildcard; tighten in production). |
| `CorsEnvVar.ALLOWED_ORIGINS` | Fallback list when `CorsEnvVar.ORIGINS` is not set. |
| `CorsEnvVar.ALLOW_CREDENTIALS` | `true` / `false` (default `CorsDefaults.DEFAULT_ALLOW_CREDENTIALS`). |
| `CorsEnvVar.ALLOW_METHODS` | Comma-separated HTTP methods (default `CorsDefaults.ALLOW_METHODS`). |
| `CorsEnvVar.ALLOW_HEADERS` | `CorsDefaults.WILDCARD` or comma-separated request header names (default `CorsDefaults.FALLBACK_ALLOW_HEADERS`). |
| `CorsEnvVar.EXPOSE_HEADERS` | Comma-separated response headers visible to browser JS (default `CorsDefaults.EXPOSE_HEADERS`). |
| `CorsEnvVar.ALLOW_ORIGIN_REGEX` | Optional regex for dynamic origins. |
| `CorsEnvVar.MAX_AGE` | Preflight cache seconds (default `CorsDefaults.DEFAULT_MAX_AGE_SECONDS`). |

Each name above is a Python constant whose **value** is the real environment key (for example, `CorsEnvVar.ORIGINS` equals ``CORS_ORIGINS``).

```python
from dtos.configuration import CorsSettingsDTO
from utilities.cors import CorsConfigUtility

settings: CorsSettingsDTO = CorsConfigUtility.load_settings_from_env()
kwargs = settings.to_middleware_kwargs()  # pass to CORSMiddleware
# or: kwargs = CorsConfigUtility.get_middleware_kwargs()
```

## Security headers

`SecurityHeadersMiddleware` (from `fastmiddleware`) is configured via `dtos.configuration.SecurityHeadersSettingsDTO` (inherits `IConfigurationDTO`), loaded by `utilities.security_headers.SecurityHeadersUtility.load_settings_from_env()` and applied in `app.py` through `SecurityHeadersUtility.get_middleware_config()`.

Defaults match the previous inline setup (HSTS, `X-Frame-Options: DENY`, CSP allowing Swagger/ReDoc assets from jsDelivr and Google Fonts). Override with:

| Variable | Purpose |
|----------|---------|
| `SecurityHeadersEnvVar.X_CONTENT_TYPE_OPTIONS` | `X-Content-Type-Options` (default `SecurityHeadersConstants.X_CONTENT_TYPE_OPTIONS`) |
| `SecurityHeadersEnvVar.X_FRAME_OPTIONS` | `X-Frame-Options` (default `SecurityHeadersConstants.X_FRAME_OPTIONS`) |
| `SecurityHeadersEnvVar.X_XSS_PROTECTION` | Legacy `X-XSS-Protection` |
| `SecurityHeadersEnvVar.REFERRER_POLICY` | `Referrer-Policy` |
| `SecurityHeadersEnvVar.ENABLE_HSTS` | `true` / `false` (default `SecurityHeadersConstants.DEFAULT_ENABLE_HSTS`) |
| `SecurityHeadersEnvVar.HSTS_MAX_AGE` | Seconds (default `SecurityHeadersConstants.DEFAULT_HSTS_MAX_AGE_SECONDS`) |
| `SecurityHeadersEnvVar.HSTS_INCLUDE_SUBDOMAINS` | `true` / `false` (default `SecurityHeadersConstants.DEFAULT_HSTS_INCLUDE_SUBDOMAINS`) |
| `SecurityHeadersEnvVar.HSTS_PRELOAD` | `true` / `false` (default `SecurityHeadersConstants.DEFAULT_HSTS_PRELOAD`) |
| `SecurityHeadersEnvVar.CONTENT_SECURITY_POLICY` | Full CSP string; if unset, `SecurityHeadersConstants.CONTENT_SECURITY_POLICY` is used |
| `SecurityHeadersEnvVar.PERMISSIONS_POLICY` | Optional `Permissions-Policy` |
| `SecurityHeadersEnvVar.CROSS_ORIGIN_OPENER_POLICY` | COOP (default `SecurityHeadersConstants.CROSS_ORIGIN_OPENER_POLICY`) |
| `SecurityHeadersEnvVar.CROSS_ORIGIN_RESOURCE_POLICY` | CORP (default `SecurityHeadersConstants.CROSS_ORIGIN_RESOURCE_POLICY`) |
| `SecurityHeadersEnvVar.CROSS_ORIGIN_EMBEDDER_POLICY` | Optional COEP |
| `SecurityHeadersEnvVar.REMOVE_SERVER_HEADER` | `true` / `false` (default `SecurityHeadersConstants.DEFAULT_REMOVE_SERVER_HEADER`) |

Each row’s constant holds the ``SECURITY_*`` string used in the environment (e.g. `SecurityHeadersEnvVar.CONTENT_SECURITY_POLICY` is ``SECURITY_CONTENT_SECURITY_POLICY``).

Programmatic access:

```python
from dtos.configuration import SecurityHeadersSettingsDTO
from utilities.security_headers import SecurityHeadersUtility

settings: SecurityHeadersSettingsDTO = SecurityHeadersUtility.load_settings_from_env()
config = settings.to_middleware_config()  # fastmiddleware.SecurityHeadersConfig
# or: config = SecurityHeadersUtility.get_middleware_config()
```

## Custom Validation

Add custom validation rules in `utilities/validator.py`:

```python
from utilities.validator import ConfigValidatorUtility

class MyValidator(ConfigValidatorUtility):
    def validate_custom_rule(self, value: str) -> tuple[bool, str]:
        """Custom validation logic."""
        if not value.startswith("custom_"):
            return False, "Value must start with 'custom_'"
        return True, ""

# In app.py
from utilities.validator import validate_config_or_exit
validate_config_or_exit(validator_class=MyValidator)
```

## Settings Management

The `config/settings.py` file uses Pydantic Settings for type-safe configuration:

```python
from pydantic_settings import ISettings

class Settings(ISettings):
    app_name: str = "FastMVC App"
    debug: bool = False
    dataI_url: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Environment-Specific Configuration

Use different `.env` files for different environments:

```bash
# .env.development
DEBUG=true
LOG_LEVEL=DEBUG

# .env.production
DEBUG=false
LOG_LEVEL=WARNING
```

Load with:

```python
from pydantic_settings import ISettings

class Settings(ISettings):
    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'development')}"
```

## Secrets Management

For production secrets, use:

1. **Environment variables** (cloud platforms)
2. **Secret managers** (AWS Secrets Manager, Azure Key Vault, etc.)
3. **Docker secrets** (for containerized deployments)

Example with AWS Secrets Manager:

```python
import boto3
from config.settings import Settings

def load_secrets_from_aws():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='my-app-secrets')
    return json.loads(response['SecretString'])

secrets = load_secrets_from_aws()
settings = Settings(
    SECRET_KEY=secrets['SECRET_KEY'],
    DATABASE_URL=secrets['DATABASE_URL']
)
```

## Configuration in Tests

Override settings for tests:

```python
import pytest
from fastapi.testclient import TestClient
from app import app
from config.settings import Settings

@pytest.fixture
def test_client():
    # Override settings for testing
    app.state.settings = Settings(
        DATABASE_URL="sqlite:///./test.db",
        SECRET_KEY="test-secret-key-for-testing-only-32chars",
        DEBUG=True
    )
    return TestClient(app)
```
