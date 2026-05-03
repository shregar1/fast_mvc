# Services

## What this module does

The **`services`** package holds **application and domain logic**: use cases, orchestration, validation that spans multiple steps, and coordination between **repositories**, caches, and external APIs. A service’s public API is typically a **`run(request_dto)`** (or similar) method that returns a **`dict`** or structured result consumed by the controller.

This layer sits between **controllers** (HTTP) and **repositories** (persistence). It is where you enforce rules like “email must be unique”, “order cannot ship if unpaid”, or “aggregate multiple reads/writes in one transaction” when your framework supports it.

## Responsibilities

| Concern | Handled here |
|--------|----------------|
| Business rules | Validation, workflows, cross-entity invariants |
| Orchestration | Multiple repositories, external calls, compensating actions |
| Logging / metrics | Operation-level context (`urn`, `api_name`, `user_id` via `IService`) |
| DTO mapping | Transform request DTOs into domain operations and results back to dicts |

## Layout (this repo)

Exact paths and inheritance are documented in **`services/rules.md`**. At a glance:

```text
services/
├── abstraction.py
├── example/                 # IExampleService + CRUD-style services
└── user/                    # IUserService + auth/MFA/phone/account flows
```

There is **no** `services/apis/v1/` directory yet; adding one should follow the same change + docs update as **`services/example/`**.

## How it fits in the stack

```
Controller → Service → Repository → Database
```

Services receive **dependencies** injected via **`dependencies/services/`** (factories) and use **DTOs** from **`dtos`** as inputs.

## Related documentation

- `abstractions/README.md` — `IService` and `run()`  
- `repositories/README.md` — data access  
- `dependencies/README.md` — service factories  

## Practices

1. **Idempotent** behavior where possible for the same logical operation.  
2. **Raise** domain-appropriate errors (mapped to HTTP by controllers or platform).  
3. **Avoid** importing FastAPI `Request` inside services; pass context via kwargs or DTOs.  
4. **Unit test** services with mocked repositories.  
5. **Do not** add pass-through modules that only alias types from `utilities/` (for example `MFAUtility` → `MFAService`); import utilities and dependency wrappers from their canonical modules. See `services/rules.md`.
