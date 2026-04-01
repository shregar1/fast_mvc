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

`CORSMiddleware` (from `fastmiddleware`, Starlette-compatible) is configured via `dtos.configuration.CorsSettingsDTO` (inherits `IConfigurationDTO`), loaded by `utilities.cors.CorsConfigUtil.load_settings_from_env()` and applied in `app.py` with `CorsConfigUtil.get_middleware_kwargs()`.

| Variable | Purpose |
|----------|---------|
| `CORS_ORIGINS` | Comma-separated allowed `Origin` values. If unset, `ALLOWED_ORIGINS` is used (e.g. Docker Compose). If both are empty, defaults to `*` (permissive; tighten in production). |
| `ALLOWED_ORIGINS` | Fallback list when `CORS_ORIGINS` is not set. |
| `CORS_ALLOW_CREDENTIALS` | `true` / `false` (default `true`). |
| `CORS_ALLOW_METHODS` | Comma-separated HTTP methods (default: GET, POST, PUT, DELETE, OPTIONS, PATCH). |
| `CORS_ALLOW_HEADERS` | `*` or comma-separated request header names (default `*`). |
| `CORS_EXPOSE_HEADERS` | Comma-separated response headers visible to browser JS (defaults include `x-transaction-urn`, `x-reference-urn`). |
| `CORS_ALLOW_ORIGIN_REGEX` | Optional regex for dynamic origins. |
| `CORS_MAX_AGE` | Preflight cache seconds (default `600`). |

```python
from dtos.configuration import CorsSettingsDTO
from utilities.cors import CorsConfigUtil

settings: CorsSettingsDTO = CorsConfigUtil.load_settings_from_env()
kwargs = settings.to_middleware_kwargs()  # pass to CORSMiddleware
# or: kwargs = CorsConfigUtil.get_middleware_kwargs()
```

## Security headers

`SecurityHeadersMiddleware` (from `fastmiddleware`) is configured via `dtos.configuration.SecurityHeadersSettingsDTO` (inherits `IConfigurationDTO`), loaded by `utilities.security_headers.load_security_headers_settings_from_env()` and applied in `app.py` through `get_security_headers_middleware_config()`.

Defaults match the previous inline setup (HSTS, `X-Frame-Options: DENY`, CSP allowing Swagger/ReDoc assets from jsDelivr and Google Fonts). Override with:

| Variable | Purpose |
|----------|---------|
| `SECURITY_X_CONTENT_TYPE_OPTIONS` | `X-Content-Type-Options` (default `nosniff`) |
| `SECURITY_X_FRAME_OPTIONS` | `X-Frame-Options` (default `DENY`) |
| `SECURITY_X_XSS_PROTECTION` | Legacy `X-XSS-Protection` |
| `SECURITY_REFERRER_POLICY` | `Referrer-Policy` |
| `SECURITY_ENABLE_HSTS` | `true` / `false` |
| `SECURITY_HSTS_MAX_AGE` | Seconds (default one year) |
| `SECURITY_HSTS_INCLUDE_SUBDOMAINS` | `true` / `false` |
| `SECURITY_HSTS_PRELOAD` | `true` / `false` |
| `SECURITY_CONTENT_SECURITY_POLICY` | Full CSP string; if unset, `SecurityHeadersConstants.CONTENT_SECURITY_POLICY` in `constants/security_headers.py` is used |
| `SECURITY_PERMISSIONS_POLICY` | Optional `Permissions-Policy` |
| `SECURITY_CROSS_ORIGIN_OPENER_POLICY` | COOP (default `SecurityHeadersConstants.CROSS_ORIGIN_OPENER_POLICY` in `constants/security_headers.py`) |
| `SECURITY_CROSS_ORIGIN_RESOURCE_POLICY` | CORP (default `SecurityHeadersConstants.CROSS_ORIGIN_RESOURCE_POLICY` in `constants/security_headers.py`) |
| `SECURITY_CROSS_ORIGIN_EMBEDDER_POLICY` | Optional COEP |
| `SECURITY_REMOVE_SERVER_HEADER` | `true` / `false` |

Programmatic access:

```python
from dtos.configuration import SecurityHeadersSettingsDTO
from utilities.security_headers import load_security_headers_settings_from_env

settings: SecurityHeadersSettingsDTO = load_security_headers_settings_from_env()
config = settings.to_middleware_config()  # fastmiddleware.SecurityHeadersConfig
```

## Custom Validation

Add custom validation rules in `utilities/validator.py`:

```python
from utilities.validator import ConfigValidator

class MyValidator(ConfigValidator):
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
    dataI_url: str | None = None
    
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
