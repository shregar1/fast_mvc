# Constants

## What this module does

The **`constants`** package is the **single source of truth** for magic strings and numbers that would otherwise be duplicated across controllers, services, and DTOs: **API logical keys** (`APILK`), **response status labels**, **default limits**, **regex** for validation, **payload type** names, and **database table** identifiers. Centralizing these values avoids typos, makes refactors safe, and gives IDEs autocompletion.

Anything that is **fixed for the whole application** (or a major version) and **not** user configuration belongs here rather than in `config/` JSON.

## Overview

The `constants` module provides centralized, type-safe constant definitions used throughout the FastMVC application. Constants prevent magic strings/numbers, enable IDE autocompletion, and make refactoring easier.

## Purpose

Using constants instead of literal values provides:

- **Type safety**: `Final[str]` annotations prevent accidental modification
- **Autocompletion**: IDE support for discovering available values
- **Refactoring**: Change a value in one place, updates everywhere
- **Documentation**: Self-documenting code with clear naming
- **Consistency**: Prevents typos and inconsistencies

## Components

### APILK (`api_lk.py`)

API Logical Keys for identifying operations.

```python
from constants.api_lk import APILK

if api_name == APILK.LOGIN:
    # Handle login-specific logic
    pass
```

| Constant | Value | Description |
|----------|-------|-------------|
| `LOGIN` | "LOGIN" | User login operations |
| `REGISTRATION` | "REGISTRATION" | New user registration |
| `LOGOUT` | "LOGOUT" | Session termination |

### APIStatus (`api_status.py`)

Standardized API response status values.

```python
from constants.api_status import APIStatus

return {
    "status": APIStatus.SUCCESS,
    "data": result
}
```

| Constant | Value | Description |
|----------|-------|-------------|
| `SUCCESS` | "SUCCESS" | Operation succeeded |
| `FAILED` | "FAILED" | Operation failed |
| `PENDING` | "PENDING" | Operation in progress |

### Default (`default.py`)

Default configuration values for all application settings.

```python
from constants.default import Default

# Use as fallback
expiry = config.get("expiry", Default.ACCESS_TOKEN_EXPIRE_MINUTES)

# Access nested security config
jwt_expiry = Default.SECURITY_CONFIGURATION["authentication"]["jwt_expiry_minutes"]
```

**Key Defaults:**
| Constant | Value | Description |
|----------|-------|-------------|
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 1440 | JWT expiry (24 hours) |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | 60 | Rate limit per minute |
| `RATE_LIMIT_REQUESTS_PER_HOUR` | 1000 | Rate limit per hour |

**Security Configuration Sections:**
- `rate_limiting`: Request rate limiting settings
- `security_headers`: HTTP security headers (HSTS, CSP, etc.)
- `input_validation`: Input sanitization rules
- `authentication`: JWT and session settings
- `cors`: Cross-Origin Resource Sharing settings

### RequestPayloadType / ResponsePayloadType (`payload_type.py`)

Content type constants for request/response handling.

```python
from constants.payload_type import RequestPayloadType, ResponsePayloadType

if payload_type == RequestPayloadType.JSON:
    data = await request.json()
```

**Request Types:**
| Constant | Value | Description |
|----------|-------|-------------|
| `JSON` | "json" | application/json |
| `FORM` | "form" | application/x-www-form-urlencoded |
| `FILES` | "files" | multipart/form-data |
| `QUERY` | "query" | URL query parameters |

**Response Types:**
| Constant | Value | Description |
|----------|-------|-------------|
| `JSON` | "json" | JSON response |
| `TEXT` | "text" | Plain text response |
| `CONTENT` | "content" | Binary/raw content |

### Security headers (`security_headers.py`)

Default strings for CSP, COOP, CORP, `X-Frame-Options`, `Referrer-Policy`, and related middleware. Used by :mod:`utilities.security_headers` and :class:`~dtos.configuration.security_headers.SecurityHeadersSettingsDTO`.

```python
from constants.security_headers import SecurityHeadersConstants

csp = SecurityHeadersConstants.CONTENT_SECURITY_POLICY
```

| Attribute | Role |
|-----------|------|
| `SecurityHeadersConstants.CONTENT_SECURITY_POLICY` | Default CSP |
| `SecurityHeadersConstants.CROSS_ORIGIN_OPENER_POLICY` | COOP default (`same-origin`) |
| `SecurityHeadersConstants.CROSS_ORIGIN_RESOURCE_POLICY` | CORP default (`same-origin`) |
| `SecurityHeadersConstants.X_*` / `REFERRER_POLICY` | Other header defaults |

### RegularExpression (`regular_expression.py`)

Pre-compiled regex patterns for validation and security.

```python
from constants.regular_expression import RegularExpression

# Validate email
if RegularExpression.EMAIL_PATTERN.match(email):
    print("Valid email")

# Check for SQL injection
for pattern in RegularExpression.DANGEROUS_SQL_INJECTION_PATTERNS:
    if re.search(pattern, user_input, re.IGNORECASE):
        raise SecurityError("Potential SQL injection detected")
```

**Validation Patterns:**
| Pattern | Description |
|---------|-------------|
| `EMAIL_PATTERN` | Email address validation |
| `PASSWORD_PATTERN` | Strong password (8+ chars, mixed case, numbers, special) |
| `PHONE_PATTERN` | International phone numbers (E.164) |
| `ALPHANUMERIC_PATTERN` | Letters, numbers, spaces, hyphens, underscores |
| `DD_MM_YYYY` | Date format DD/MM/YYYY |

**Security Patterns:**
| Pattern | Description |
|---------|-------------|
| `DANGEROUS_SQL_INJECTION_PATTERNS` | SQL injection detection |
| `DANGEROUS_XSS_PATTERNS` | Cross-site scripting detection |
| `DANGEROUS_PATH_TRAVERSAL_PATTERNS` | Directory traversal detection |

### Table (`db/table.py`)

DataI table name constants.

```python
from constants.db.table import Table

class User(I):
    __tablename__ = Table.USER
```

| Constant | Value | Description |
|----------|-------|-------------|
| `USER` | "user" | User accounts table |

## File Structure

```
constants/
├── __init__.py              # Package exports
├── api_lk.py               # API logical keys
├── api_status.py           # Response status values
├── default.py              # Default configuration values
├── payload_type.py         # Request/response content types
├── security_headers.py     # CSP, COOP, CORP, and related header defaults
├── regular_expression.py   # Validation regex patterns
├── db/
│   ├── __init__.py
│   └── table.py            # DataI table names
└── README.md               # This documentation
```

## Best Practices

1. **Use Final type hints**: All constants should be `Final[T]` to prevent modification
2. **Descriptive names**: Use clear, self-documenting constant names
3. **Group related constants**: Use classes to group related values
4. **Add docstrings**: Document what each constant is used for
5. **Import specifically**: `from constants.api_status import APIStatus` not `from constants import *`

## Adding New Constants

1. Determine the appropriate file or create a new one
2. Add the constant with `Final[T]` type annotation
3. Add a docstring explaining its purpose
4. Update this README with the new constant

```python
from typing import Final

class MyConstants:
    """Description of this constant group."""
    
    MY_CONSTANT: Final[str] = "value"
    """Description of what this constant is for."""
```
