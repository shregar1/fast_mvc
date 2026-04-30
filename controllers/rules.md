# Controller Rules

Controllers are thin HTTP adapters. Keep business logic out of them.

## Directory Structure

All domain API controllers live under `controllers/apis/v1/`. Auth controllers stay at the top level.

```
controllers/
  apis/
    __init__.py             # APIs router (prefix="/apis"), includes v1 router
    abstraction.py          # IAPIController
    json_api_controller.py  # JSONAPIController (root JSON base)
    v1/
      __init__.py           # v1 router (prefix="/v1"), includes all domain routers
      abstraction.py        # IAPIV1Controller
      <domain>/
        __init__.py         # domain router (prefix="/<domain>"), imports & wires routes
        abstraction.py      # IDomainController(JSONAPIController)
        _helpers.py         # shared repo/service factory helpers (optional)
        <action>.py         # one controller class per file
        ...
  auth/                     # auth stays outside apis/v1
    __init__.py
    abstraction.py          # IAuthController(IController)
    user/
      abstraction.py        # IUserController(JSONAPIController)
      login.py
      ...
```

## Router Nesting

Routers are nested three levels deep. `app.py` imports a single aggregated router:

```
app.py
  └── APIsRouter (prefix="/apis")            ← controllers/apis/__init__.py
        └── v1_router (prefix="/v1")         ← controllers/apis/v1/__init__.py
              ├── <domain>_router (/<domain>) ← controllers/apis/v1/<domain>/__init__.py
              └── ...
```

All domain endpoints are served under `/apis/v1/<domain>/...`.

When adding a new domain:
1. Create `controllers/apis/v1/<domain>/` with `__init__.py`, `abstraction.py`, and controller files.
2. Include the domain router in `controllers/apis/v1/__init__.py`.

## Inheritance Hierarchy

```
IController (abstractions/controller.py)
  └── JSONAPIController (controllers/apis/json_api_controller.py)
        ├── IAPIController (controllers/apis/abstraction.py)
        │     └── IAPIV1Controller (controllers/apis/v1/abstraction.py)
        └── IUserController (controllers/auth/user/abstraction.py)
```

Every domain controller **must** extend its domain abstraction, not `JSONAPIController` directly.

## Structure

1. **Extend the domain abstraction** — domain controllers extend their domain abstraction, auth user routes extend `IUserController`, etc. Never extend `JSONAPIController` directly from a controller file.
2. **`__init__` only sets `api_name`** — forward everything else to `super().__init__(..., *args, **kwargs)`. Never shadow `_urn`, `_user_id`, etc. — the parent setters already handle it.
3. **One controller class per file** — `post` / `get` / `put` / `delete`. No private helpers that contain business rules — push those into a service.
4. **Shared helpers in `_helpers.py`** — domain-specific `_repo()` and `_svc()` factory wrappers live in `_helpers.py` alongside the controller files. Controllers import these rather than duplicating the boilerplate.

## Handler Body (mandatory order)

```python
async def post(self, request: Request, request_payload: XxxDTO,
               session: Session = Depends(DBDependency.derive),
               service_factory: Callable = Depends(XxxServiceDependency.derive),
               dictionary_utility: DictionaryUtility = Depends(DictionaryUtilityDependency.derive),
               ...):
    try:
        self.bind_request_context(request, dictionary_utility_factory=dictionary_utility)
        # instantiate repos with session
        # await self.validate_request(...)
        response_dto = await service_factory(
            urn=self.urn, user_urn=self.user_urn, api_name=self.api_name,
            user_id=self.user_id, ...,
        ).run(request_dto=request_payload)
        http_status = HTTPStatus.OK
    except Exception as err:
        response_dto, http_status = self.handle_exception(
            err, request, event_name="x.y", session=session,
            force_http_ok=False, fallback_message="...",
        )

    content = (
        self.dictionary_utility.convert_dict_keys_to_camel_case(response_dto.model_dump())
        if self.dictionary_utility is not None
        else response_dto.model_dump()
    )
    return JSONResponse(content=content, status_code=http_status)
```

## Do

- Use `bind_request_context(request, ...)` at the top of every handler — don't re-implement the URN/user_id/logger lifting.
- Use `handle_exception(...)` for the `except Exception` branch — never format error envelopes inline.
- Get services and repositories via `Depends(XxxDependency.derive)` factories — never instantiate directly.
- Apply `convert_dict_keys_to_camel_case` to the response body before returning.
- Pass `force_http_ok=False` on new-style endpoints; legacy auth endpoints may set `True` for contract compatibility.
- Wrap side-effects (audit, webhook, welcome email) in `try/except` with a warning log — they must never break the success path.
- Register routes in the domain `__init__.py` using `router.add_api_route(...)`.
- Include new domain routers in `controllers/apis/v1/__init__.py` — that is the only place domain routers are aggregated.

## Don't

- Don't do SQLAlchemy queries in a controller — go through a repository.
- Don't raise `HTTPException` — raise typed errors from `fastx_platform.errors` and let `handle_exception` translate them.
- Don't construct `BaseResponseDTO` in the happy path — that's the service's job.
- Don't create private methods on the controller that touch the DB session.
- Don't pass `self.user_id or ""` — `user_id` is `int | None`; let `None` flow through.
- Don't add response-field renaming logic — if the DTO key is wrong, fix the DTO.
- Don't catch narrow exceptions to return inline envelopes — one `except Exception` + `handle_exception` is the pattern.
- Don't put multiple controller classes in one file — one class per file, always.
- Don't import domain routers directly in `app.py` — they flow through the `apis → v1` chain.
- Don't extend `JSONAPIController` directly — extend the domain abstraction.
