# Service Rules

Services hold business logic. They orchestrate repositories, utilities, and external calls — they are the only layer allowed to encode policy.

## Directory Structure

API domain services live under `services/apis/v1/`. Auth services live under `services/auth/user/`.

```text
services/
  __init__.py
  abstraction.py             # IService (root service interface)
  apis/
    __init__.py
    v1/
      __init__.py
      <domain>/
        __init__.py          # re-exports all service classes
        abstraction.py       # IDomainService(IService)
        _helpers.py          # domain-specific error factories (optional)
        <action>.py          # one service class per file
        ...
  auth/
    __init__.py
    user/                    # mirrors controllers/auth/user/
      __init__.py            # re-exports all top-level user service classes
      abstraction.py         # IUserService(IService)
      login.py               # one service class per file
      register.py
      logout.py
      fetch.py
      refresh_token.py
      forgot_password.py
      reset_password.py
      subscription.py
      token_issuance.py
      mfa/
        __init__.py          # re-exports all MFA service classes
        abstraction.py       # IMFAService(IUserService)
        setup.py
        verify.py
        disable.py
        status.py
        qr_code.py
      phone/
        __init__.py          # re-exports all phone service classes
        abstraction.py       # IPhoneService(IUserService)
        send_otp.py
        verify_otp.py
      account/
        __init__.py          # re-exports all account service classes
        abstraction.py       # IAccountService(IUserService)
        send_verification_email.py
        verify_email.py
        verify_mfa.py
```

This mirrors the controller hierarchy (`controllers/apis/v1/<domain>/` and `controllers/auth/user/`).

## Inheritance Hierarchy

```text
FrameworkService (abstractions/service.py)
  └── IService (services/abstraction.py)
        ├── IDomainService (services/apis/v1/<domain>/abstraction.py)
        └── IUserService (services/auth/user/abstraction.py)
              ├── IMFAService (services/auth/user/mfa/abstraction.py)
              ├── IPhoneService (services/auth/user/phone/abstraction.py)
              └── IAccountService (services/auth/user/account/abstraction.py)
```

Every service class **must** extend its domain abstraction, not `IService` directly. User sub-domain services extend their sub-domain abstraction (e.g. MFA services extend `IMFAService`, not `IUserService`).

## Structure

1. **Extend the domain abstraction** — domain services extend their domain abstraction, user services extend `IUserService`, etc. Never extend `IService` directly from a service file.
2. **One service class per file** — `UserLoginService.run()`, not `UserService.login()/logout()/register()`. One class, one verb, one file.
3. **Constructor takes dependencies, not primitives** — repositories, utilities, and context fields (`urn`, `user_urn`, `api_name`, `user_id`). Forward `*args, **kwargs` to `super().__init__(...)`.
4. **Entry point is `async def run(self, request_dto)`** — returns a `BaseResponseDTO`.
5. **Domain-specific helpers in `_helpers.py`** — error factories and internal base classes live in `_helpers.py`. Only create `_helpers.py` when the domain needs its own helpers; shared behaviour belongs on the abstraction at the appropriate layer.

When adding a new API domain:

1. Create `services/apis/v1/<domain>/` with `__init__.py`, `abstraction.py`, and one service file per use case.
2. The domain abstraction extends `IService` and injects the domain repository.
3. Re-export all service classes in the domain `__init__.py`.
4. Create matching dependency factories in `dependencies/services/<domain>/`.

## Do

- Validate business invariants here; raise typed errors (`BadInputError`, `ConflictError`, `NotFoundError`, `UnauthorizedError`, `RateLimitError`, `ServiceUnavailableError`, `UnexpectedResponseError`).
- Put every external call (SMTP, Redis, webhook, 3rd-party HTTP) behind a utility and assume it can fail — raise `ServiceUnavailableError` or `UnexpectedResponseError` on failure.
- Keep repository access through the injected repository instance — never open a new session.
- Log at `info` for happy-path milestones, `warning` for handled failures, `error` only for unrecoverable bugs.
- Make services stateless across calls — everything lives on the injected context and inputs.
- Put shared behaviour on the abstraction at the appropriate layer — `IService` for all services, domain abstraction for domain-wide behaviour.

## Don't

- Don't touch `request.state` — if you need a field, take it as a constructor arg.
- Don't import `fastapi` — services are transport-agnostic. No `Request`, no `JSONResponse`, no `HTTPException`.
- Don't catch exceptions to return a "FAILED" DTO — raise typed errors; the controller's `handle_exception` is the single error translator.
- Don't commit/rollback the session — the repository or the unit-of-work owns the transaction boundary.
- Don't instantiate another service inside a service — compose via the dependency factory or split the use case.
- Don't cache context on the class (`UserLoginService.current_user`) — pass it through explicitly.
- Don't take `*_factory` callables — services receive already-constructed dependencies.
- Don't put API domain services at the top level — they belong in `services/apis/v1/<domain>/`.
- Don't put auth services inside `apis/v1/` — they stay at `services/auth/user/`.
- Don't put multiple service classes in one file — one class per file, always.
- Don't extend `IService` directly from a service file — extend the domain abstraction.

## Dependency Factory Contract

Every service must have a matching `dependencies/services/.../<service>.py` that exposes a `XxxServiceDependency` with a `derive()` classmethod returning a callable:

```python
def factory(urn, user_urn, api_name, user_id, **deps) -> XxxService: ...
```

The controller calls this factory; the service's `__init__` signature must stay compatible with it.
