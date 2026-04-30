# Utility Rules

Utilities are stateless-ish helpers: JWT, dictionary conversion, hashing, JSON-Web-Key loading, HTTP client wrappers, email, audit, client-IP extraction, etc. They're the glue between services and external tech.

## Structure

1. **Every utility file must contain exactly one class** that inherits from `IUtility` (from `abstractions.utility`). No standalone functions at module level.
2. **Class utilities take context in `__init__`** — `urn`, `user_urn`, `api_name`, `user_id`. Forward `*args, **kwargs` to `super().__init__(...)`.
3. **Stateless helpers use `@staticmethod`** — if a method doesn't need per-request context, make it a static method on the class rather than a standalone function.

```python
from abstractions.utility import IUtility

class AuditUtility(IUtility):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def log_audit(session, action, resource_type, *, actor_id=None, ...):
        ...
```

## Inheritance

```
IUtility (abstractions/utility.py)
  ├── AuditUtility (utilities/audit.py)
  ├── DateTimeUtility (utilities/datetime.py)
  ├── DictionaryUtility (utilities/dictionary.py)
  ├── EnvironmentParserUtility (utilities/env.py)
  ├── JWTUtility (utilities/jwt.py)
  ├── MFAUtility (utilities/mfa.py)
  ├── PhoneOtpUtility (utilities/phone_otp.py)
  ├── RequestUtility (utilities/request_utils.py)
  ├── SecurityUtility (utilities/security.py)
  ├── SecurityHeadersUtility (utilities/security_headers.py)
  ├── StringUtility (utilities/string.py)
  ├── SystemUtility (utilities/system.py)
  ├── ConfigValidatorUtility (utilities/validator.py)
  └── WebhookDispatcherUtility (utilities/webhook_dispatcher.py)
```

Every utility class **must** extend `IUtility`. No exceptions.

## Do

- Make every utility injectable via a dependency factory in `dependencies/utilities/<x>.py` — that's how controllers get per-request instances.
- Raise typed errors from `fastx_platform.errors` (`UnexpectedResponseError`, `ServiceUnavailableError`) on external failures — never leak raw `requests`/`httpx`/`smtplib` exceptions.
- Treat external I/O as failable: timeouts, retries, and a `try/except` that surfaces a typed error.
- Log at `debug` for normal operation, `warning` when a retryable call fails, `error` when the helper gives up.
- Keep return shapes simple — dict, DTO, or primitive. No SQLAlchemy objects, no FastAPI types.
- Use `@staticmethod` for methods that don't need instance state — callers can invoke them directly on the class without instantiation.

## Don't

- Don't put standalone functions at module level — wrap them as `@staticmethod` on the utility class.
- Don't touch the DB session. If you need persistence, you belong in a repository.
- Don't import controllers or services — utilities are leaves in the dependency graph.
- Don't cache on a module-level mutable (`_cache = {}`) without a TTL or explicit invalidation path.
- Don't read environment variables at call time — read them once at module import (or use the `config/` layer) so tests can patch cleanly.
- Don't swallow exceptions — convert them, don't hide them.

## Dependency Factory Contract

Every injectable utility must have a matching `dependencies/utilities/<x>.py`:

```python
class XxxUtilityDependency:
    @classmethod
    def derive(cls) -> Callable[..., XxxUtility]:
        def factory(urn, user_urn, api_name, user_id) -> XxxUtility:
            return XxxUtility(urn=urn, user_urn=user_urn,
                              api_name=api_name, user_id=user_id)
        return factory
```

Controllers then `Depends(XxxUtilityDependency.derive)` and pass the factory into `bind_request_context(...)`.

## File Layout

```
utilities/
  __init__.py               # re-exports all utility classes
  audit.py                  # AuditUtility
  datetime.py               # DateTimeUtility
  dictionary.py             # DictionaryUtility
  env.py                    # EnvironmentParserUtility
  jwt.py                    # JWTUtility
  mfa.py                    # MFAUtility
  phone_otp.py              # PhoneOtpUtility
  request_utils.py          # RequestUtility
  security.py               # SecurityUtility
  security_headers.py       # SecurityHeadersUtility
  string.py                 # StringUtility
  system.py                 # SystemUtility
  validator.py              # ConfigValidatorUtility
  webhook_dispatcher.py     # WebhookDispatcherUtility
```

One class per file. File name matches the utility's purpose. Class name follows `XxxUtility` convention.
