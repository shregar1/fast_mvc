# Data Transfer Objects (DTOs)

## What this module does

The **`dtos`** package defines **Pydantic models** for **HTTP request bodies**, **query parameters**, and **response envelopes**. It is the **contract** between clients and the API: validation, OpenAPI schema generation, and safe defaults happen here before code reaches **controllers** and **services**.

Request DTOs often inherit from **`IRequestDTO`** (reference numbers, shared validators); responses use **`IResponseDTO`** for a consistent **`transactionUrn`**, **`status`**, **`data`**, and **`errors`** shape. **Configuration DTOs** under **`dtos/configuration/`** inherit **`IConfigurationDTO`** and describe typed, env-backed settings (e.g. CORS and security headers) consumed by **`config.*`** loaders.

## Nested folders and leaf filenames

When DTOs are grouped by **segment** (e.g. `dtos/requests/item/`), **leaf module names stay short**; the path already encodes the resource. Use **verb or role** filenames such as **`create.py`**, **`update.py`**, **`fetch.py`** — not `create_item_request_dto.py` under `item/`.

**Class names** remain fully explicit (`CreateItemRequestDTO`, `UpdateItemRequestDTO`). See [**New API scaffolding**](../docs/guide/new-api-scaffolding.md#leaf-file-naming-nested-folders) for the generator/CLI convention.

## One concrete class per file

- **Default**: **one** concrete Pydantic **model class** per **module** (one **purpose** per file: create, update, delete, etc.).
- **Nested models**: Small helper models that exist **only** to compose a parent DTO (e.g. nested `Address` fields) **may** live in the **same file** as that parent. If a type is **reused** across requests, give it its own module.
- **Abstractions**: Segment-level bases (`abstraction.py`, `IRequestExampleDTO`) are separate from concrete bodies.

See [**New API scaffolding — One concrete class per file**](../docs/guide/new-api-scaffolding.md#one-concrete-class-per-file-dtos).

## Overview

The `dtos` module contains Pydantic models for data validation, serialization, and documentation. DTOs ensure type-safe data transfer between layers of the application.

## Purpose

**Data Transfer Objects (DTOs)** provide:

- **Type validation**: Automatic validation of incoming data
- **Serialization**: Convert between Python objects and JSON
- **Documentation**: Self-documenting API contracts
- **Security**: Input sanitization and security validation
- **IDE support**: Autocompletion and type checking

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     HTTP Request                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Request DTOs                              │
│     (Validation, Sanitization, Type Conversion)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Controller Layer                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Service Layer                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Repository Layer                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       DB Model Layer                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Response DTOs                              │
│          (Standardized Response Structure)                   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Base models

#### ApplicationBaseModel (`base.py`)

Pydantic base model for DTOs with optional sanitization and security checks.

```python
from dtos.base import ApplicationBaseModel

class MyRequestDTO(ApplicationBaseModel):
    username: str
    email: str

# Input is automatically sanitized
dto = MyRequestDTO(username="  john  ", email="USER@Example.com")
dto.username  # "john" (trimmed)

# Security validation
result = dto.validate_security()
if not result['is_valid']:
    print(result['issues'])
```

**Features:**

- Automatic string sanitization
- SQL injection detection
- XSS attack detection
- Path traversal detection
- Extra fields rejected

### Request DTOs

#### IRequestDTO (`requests/abstraction.py`)

I class for all request DTOs.

```python
from dtos.requests.abstraction import IRequestDTO

class MyRequestDTO(IRequestDTO):
    custom_field: str

# Requires valid UUID reference_urn
request = MyRequestDTO(
    reference_urn="550e8400-e29b-41d4-a716-446655440000",
    custom_field="value"
)
```

#### UserLoginRequestDTO (`requests/user/login.py`)

```python
from dtos.requests.user.login import UserLoginRequestDTO

login = UserLoginRequestDTO(
    reference_urn="550e8400-e29b-41d4-a716-446655440000",
    email="user@example.com",
    password="SecureP@ss123"
)
```

**Validation:**

- Email: Valid format, normalized
- Password: Non-empty, meets strength requirements

#### UserRegistrationRequestDTO (`requests/user/registration.py`)

```python
from dtos.requests.user.registration import UserRegistrationRequestDTO

register = UserRegistrationRequestDTO(
    reference_urn="550e8400-e29b-41d4-a716-446655440000",
    email="newuser@example.com",
    password="SecureP@ss123"
)
```

#### UserLogoutRequestDTO (`requests/user/logout.py`)

```python
from dtos.requests.user.logout import UserLogoutRequestDTO

logout = UserLogoutRequestDTO(
    reference_urn="550e8400-e29b-41d4-a716-446655440000"
)
```

### Response DTOs

#### IResponseDTO (`responses/I.py`)

Standard response structure for all endpoints.

```python
from dtos.responses.abstraction import IResponseDTO
from constants.api_status import APIStatus

# Success response
response = IResponseDTO(
    transactionUrn="urn:req:abc123",
    status=APIStatus.SUCCESS,
    responseMessage="Operation completed",
    responseKey="success_operation",
    data={"result": "value"}
)

# Error response
error_response = IResponseDTO(
    transactionUrn="urn:req:abc123",
    status=APIStatus.FAILED,
    responseMessage="Validation failed",
    responseKey="error_validation",
    data={},
    errors=[{"field": "email", "message": "Invalid format"}]
)
```

**JSON Output:**

```json
{
    "transactionUrn": "urn:req:abc123",
    "status": "SUCCESS",
    "responseMessage": "Operation completed",
    "responseKey": "success_operation",
    "data": {"result": "value"},
    "errors": null
}
```

### Configuration DTOs

#### CacheConfigurationDTO (`configurations/cache.py`)

```python
class CacheConfigurationDTO(IModel):
    host: str      # Redis host
    port: int      # Redis port
    password: str  # Redis password
```

#### DBConfigurationDTO (`configurations/db.py`)

```python
class DBConfigurationDTO(IModel):
    user_name: str
    password: str
    host: str
    port: int
    database: str
    connection_string: str
```

#### SecurityConfigurationDTO (`configurations/security.py`)

Nested configuration for all security settings:

```python
class SecurityConfigurationDTO(IModel):
    rate_limiting: RateLimitingConfig
    security_headers: SecurityHeadersConfigDTO
    input_validation: InputValidationConfigDTO
    authentication: AuthenticationConfigDTO
    cors: CORSConfigDTO
```

## File Structure

```text
dtos/
├── __init__.py
├── README.md
├── base.py                   # ApplicationBaseModel
├── configurations/
│   ├── __init__.py
│   ├── cache.py                 # Cache configuration DTO
│   ├── db.py                    # DataI configuration DTO
│   └── security.py              # Security configuration DTOs
├── requests/
│   ├── __init__.py
│   ├── abstraction.py           # IRequestDTO I class
│   └── user/
│       ├── __init__.py
│       ├── login.py             # Login request DTO
│       ├── logout.py            # Logout request DTO
│       └── registration.py      # Registration request DTO
└── responses/
    ├── __init__.py
    └── I.py                  # IResponseDTO
```

## Password Validation Rules

The password validation in request DTOs enforces:

| Requirement | Description |
|-------------|-------------|
| Minimum length | At least 8 characters |
| Uppercase | At least one uppercase letter (A-Z) |
| Lowercase | At least one lowercase letter (a-z) |
| Digit | At least one number (0-9) |
| Special char | At least one of: @$!%*?& |

## Best Practices

1. **Inherit from appropriate I**: Use `ApplicationBaseModel` when you need sanitization/security helpers; otherwise use `IRequestDTO` and the request hierarchy
2. **Add field validators**: Custom validation for business rules
3. **Use type hints**: Pydantic uses them for validation
4. **Document fields**: Add docstrings for API documentation
5. **Keep DTOs focused**: One DTO per specific use case
6. **Validate early**: DTOs catch errors at the API boundary

## Adding New DTOs

1. Create the DTO file in the appropriate directory
2. Inherit from `IRequestDTO` / `ApplicationBaseModel` for requests as appropriate
3. Add field validators as needed
4. Add comprehensive docstrings
5. Update this README
