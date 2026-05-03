# Service Rules

Services hold business logic. They orchestrate repositories, utilities, and external calls — they are the only layer allowed to encode policy.

This document describes **`fastx_mvc/services/` as it exists in git**. If you add or remove packages, update this file in the same change.

## Directory layout (authoritative)

There is **no** `services/apis/v1/` directory in this repository today. Layout is:

```text
services/
  __init__.py
  abstraction.py
  example/
    __init__.py
    abstraction.py      # IExampleService(IService)
    create.py
    delete.py
    fetch.py
    fetch_all.py
    update.py
  user/
    __init__.py
    abstraction.py      # IUserService(IService)
    fetch.py
    forgot_password.py
    login.py
    logout.py
    phone_verify_service.py
    refresh_token.py
    register.py
    reset_password.py
    subscription.py
    token_issuance.py
    mfa/
      __init__.py
      disable.py
      qr_code.py
      setup.py
      status.py
      verify.py
    phone/
      __init__.py
      send_otp.py
      verify_otp.py
    account/
      __init__.py
      send_verification_email.py
      verify_email.py
      verify_mfa.py
```

Controllers live under `controllers/auth/user/` and `controllers/apis/v1/`; only the parts above exist under `services/`.

## Inheritance (matches code today)

```text
abstractions.service.IService
  └── services.abstraction.IService
        ├── services.user.abstraction.IUserService
        │     └── most service classes under services/user/
        └── services.example.abstraction.IExampleService
              └── *Service classes under services/example/
```

There are **no** `IMFAService`, `IPhoneService`, or `IAccountService` types in this tree. Subfolders `user/mfa/`, `user/phone/`, and `user/account/` do **not** define `abstraction.py`; their services subclass **`IUserService`** when they participate in the standard service base (see exceptions).

**Plain classes (do not subclass `IUserService`):** `ForgotPasswordService`, `ResetPasswordService`, `PhoneSendOtpService`, `PhoneVerifyOtpService`, `SendVerificationEmailService`, `VerifyEmailService`. New work should prefer extending `IUserService` unless there is a strong reason not to.

## Imports (no thin re-exports)

Do not add modules under `services/` that only re-export types from `utilities/` under a `*Service` alias (removed shims: `services/mfa.py`, `services/user/phone_otp.py`). Use **`MFAUtility`** from `fastx_platform.core.utils` (the `utilities` package re-exports it for convenience), **`PhoneOtpUtility`** from `utilities.phone_otp`, and **`MFAUtilityDependency`** from `dependencies/services/mfa.py` in controllers.

## Structure

1. **Extend the right abstraction** — example-domain services extend `IExampleService`; user-domain services extend `IUserService` unless they are one of the legacy plain classes listed above.
2. **One service class per file** — one class, one verb, one file.
3. **Constructor takes dependencies, not primitives** — repositories, utilities, and context fields (`urn`, `user_urn`, `api_name`, `user_id`). Forward `*args, **kwargs` to `super().__init__(...)` when using `IUserService` / `IExampleService`.
4. **Entry point is `async def run(self, request_dto)`** — returns a `BaseResponseDTO` (or project equivalent).
5. **Domain-specific helpers** — use `_helpers.py` only when a domain under `services/` needs shared helpers; this repo’s `example/` domain does not use `_helpers.py` yet.

## Adding `services/apis/v1/` (not present yet)

When you introduce API-domain services, add `services/apis/v1/<domain>/` with `abstraction.py` defining `IDomainService(IService)`, one file per use case, package `__init__.py` exports, and matching `dependencies/services/...` factories — mirror the existing **`services/example/`** pattern.

## Do

- Validate business invariants here; raise typed errors (`BadInputError`, `ConflictError`, `NotFoundError`, `UnauthorizedError`, `RateLimitError`, `ServiceUnavailableError`, `UnexpectedResponseError`).
- Put every external call (SMTP, Redis, webhook, 3rd-party HTTP) behind a utility and assume it can fail — raise `ServiceUnavailableError` or `UnexpectedResponseError` on failure.
- Keep repository access through the injected repository instance — never open a new session.
- Log at `info` for happy-path milestones, `warning` for handled failures, `error` only for unrecoverable bugs.
- Make services stateless across calls — everything lives on the injected context and inputs.
- Put shared behaviour on the abstraction at the appropriate layer — `IService` for all services, `IUserService` / `IExampleService` / future domain bases for shared user/example/domain behaviour.

## Don't

- Don't touch `request.state` — if you need a field, take it as a constructor arg.
- Don't import `fastapi` — services are transport-agnostic. No `Request`, no `JSONResponse`, no `HTTPException`.
- Don't catch exceptions to return a "FAILED" DTO — raise typed errors; the controller's `handle_exception` is the single error translator.
- Don't commit/rollback the session — the repository or the unit-of-work owns the transaction boundary.
- Don't instantiate another service inside a service — compose via the dependency factory or split the use case.
- Don't cache context on the class — pass it through explicitly.
- Don't take `*_factory` callables — services receive already-constructed dependencies.
- Don't add pass-through `services/*.py` files that only alias `utilities.*` types as `*Service`.
- Don't put multiple service classes in one file — one class per file, always.
- Don't document subdomains as having `abstraction.py` until those files exist.

## Dependency factory contract

Every service must have a matching `dependencies/services/.../<service>.py` that exposes a `XxxServiceDependency` with a `derive()` classmethod returning a callable:

```python
def factory(urn, user_urn, api_name, user_id, **deps) -> XxxService: ...
```

The controller calls this factory; the service's `__init__` signature must stay compatible with it.
