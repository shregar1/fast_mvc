# Utility Rules

Utilities are helpers for JWT, dictionaries, startup/config, HTTP, MFA/TOTP, phone OTP, etc. This document describes **`fastx_mvc/utilities/` as it exists in git**. Update it when you add or rename modules.

## Reality: mixed patterns

Not every file here is an **`IUtility`** subclass. The tree includes:

- **Classes that subclass `IUtility`** — see list below.
- **Classes that do not subclass `IUtility`** — e.g. `DictionaryUtility`, `JWTUtility` (plain classes with similar constructor context).
- **Module-level functions only** — e.g. `audit.py`, `auth.py`, `security.py`, `webhook_dispatcher.py`, `database_url.py`, `redis_url.py`, `request_utils.py`.

Do not assume “one `IUtility` class per file” for the whole package; use the inventory below.

## `IUtility` subclasses (authoritative)

These modules define exactly one public class that extends **`IUtility`** (`abstractions.utility`):

- **`cors.py`** — `CorsConfigUtility`
- **`datetime.py`** — `DateTimeUtility`
- **`env.py`** — `EnvironmentParserUtility`
- **`mfa.py`** — `MFAUtility`
- **`phone_otp.py`** — `PhoneOtpUtility`
- **`security_headers.py`** — `SecurityHeadersUtility`
- **`string.py`** — `StringUtility`
- **`system.py`** — `SystemUtility`
- **`validator.py`** — `ConfigValidatorUtility`

## Other modules (not `IUtility` subclasses)

- **`audit.py`** — `log_audit(...)`
- **`auth.py`** — `constant_time_compare`, `parse_basic_authorization`
- **`database_url.py`** — `build_postgresql_url_from_components`, `resolve_database_url`
- **`dictionary.py`** — `DictionaryUtility` (plain class)
- **`jwt.py`** — `JWTUtility` (plain class)
- **`redis_url.py`** — `build_redis_url_from_components`, `resolve_redis_url`
- **`request_utils.py`** — `get_client_ip`
- **`security.py`** — `hash_password`, `verify_password`
- **`webhook_dispatcher.py`** — `dispatch_webhook_event`

## Inheritance (IUtility line only)

```text
IUtility (abstractions/utility.py)
  ├── CorsConfigUtility (utilities/cors.py)
  ├── DateTimeUtility (utilities/datetime.py)
  ├── EnvironmentParserUtility (utilities/env.py)
  ├── MFAUtility (utilities/mfa.py)
  ├── PhoneOtpUtility (utilities/phone_otp.py)
  ├── SecurityHeadersUtility (utilities/security_headers.py)
  ├── StringUtility (utilities/string.py)
  ├── SystemUtility (utilities/system.py)
  └── ConfigValidatorUtility (utilities/validator.py)
```

## Consumers

Import from **`utilities/<module>.py`** or from **`utilities/__init__.py`** (barrel). Do not add **`services/`** shims that re-export the same type under another name.

Controllers inject MFA via **`dependencies/services/mfa.py`** (`MFAUtilityDependency`), not a duplicate export.

## Do

- For **new** injectable request-scoped helpers, prefer subclassing **`IUtility`** and adding **`dependencies/utilities/<x>.py`** with `derive()` returning a factory — matches existing MFA/phone OTP wiring.
- Raise typed errors from `fastx_platform.errors` on external failures — never leak raw client-library exceptions.
- Treat external I/O as failable: timeouts, retries, and typed errors on exhaustion.
- Log at `debug` for normal operation, `warning` when a retryable call fails, `error` when the helper gives up.
- Keep return shapes simple — dict, DTO, or primitive. No SQLAlchemy objects, no FastAPI types on utility boundaries.

## Don't

- Don't claim every file under `utilities/` is a single `IUtility` — use the lists above.
- Don't add `services/mfa.py`-style aliases — `MFAUtility` and `PhoneOtpUtility` live here.
- Don't import controllers or services — utilities are leaves in the dependency graph.
- Don't read environment variables at call time for hot paths without a clear pattern — prefer import-time or `config/` for stable tests.

## Dependency factory contract

Injectable `IUtility` types use **`dependencies/utilities/<x>.py`**:

```python
class XxxUtilityDependency:
    @classmethod
    def derive(cls) -> Callable[..., XxxUtility]:
        def factory(urn, user_urn, api_name, user_id) -> XxxUtility:
            return XxxUtility(urn=urn, user_urn=user_urn,
                              api_name=api_name, user_id=user_id)
        return factory
```

Controllers `Depends(XxxUtilityDependency.derive)` and pass the factory into `bind_request_context(...)` where applicable.

## File layout (authoritative)

```text
utilities/
  __init__.py
  audit.py
  auth.py
  cors.py
  database_url.py
  datetime.py
  dictionary.py
  env.py
  jwt.py
  mfa.py
  phone_otp.py
  redis_url.py
  request_utils.py
  security.py
  security_headers.py
  string.py
  system.py
  validator.py
  webhook_dispatcher.py
```
