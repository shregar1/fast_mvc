# Error Rules

Errors are typed exceptions that flow from services/repositories up through controllers, where `handle_exception` translates them into structured JSON envelopes.

## Structure

1. **One error class per file** — each custom error shim gets its own file in `errors/`.
2. **Only create files for custom shims** — errors that need default values or extra behaviour (e.g. defaulting `httpStatusCode`). Do NOT create wrapper files that just re-export a `fastx_platform.errors` class unchanged.
3. **Re-export upstream errors in `__init__.py`** — errors from `fastx_platform.errors` that need no customisation are re-exported directly in `errors/__init__.py` so services can import everything from one place.
4. **Services import from `errors`** — always `from errors import NotFoundError`, never from `errors.not_found` or `fastx_platform.errors` directly.

## When to create a new error file

Create `errors/<name>.py` only when you need to:
- Default a parameter (e.g. `httpStatusCode=404`)
- Add extra fields or behaviour
- Subclass an upstream error with custom logic

If the upstream `fastx_platform.errors` class is fine as-is, just add a re-export line in `errors/__init__.py`.

## File Layout

```
errors/
  __init__.py               # re-exports all errors (custom + upstream)
  rules.md
  bad_input.py              # BadInputError (shim, defaults httpStatusCode=400)
  config_validation.py      # ConfigValidationError (standalone, no upstream parent)
  not_found.py              # NotFoundError (shim, defaults httpStatusCode=404)
  unexpected_response.py    # UnexpectedResponseError (shim, defaults httpStatusCode=502)
```

Upstream errors re-exported directly in `__init__.py` (no wrapper file):
- `ConflictError`
- `ForbiddenError`
- `RateLimitError`
- `ServiceUnavailableError`
- `UnauthorizedError`

## Custom shim pattern

```python
from fastx_platform.errors import NotFoundError as _NotFoundError


class NotFoundError(_NotFoundError):
    def __init__(self, *, responseMessage: str, responseKey: str,
                 httpStatusCode: int = 404) -> None:
        super().__init__(
            responseMessage=responseMessage, responseKey=responseKey,
            httpStatusCode=httpStatusCode,
        )
```

## Do

- Import errors from `errors` package: `from errors import NotFoundError`.
- Raise typed errors from services — controllers catch them via `handle_exception`.
- Keep error classes thin — no business logic, no DB access.

## Don't

- Don't create a file that just does `from fastx_platform.errors import X` — put that in `__init__.py`.
- Don't import directly from `fastx_platform.errors` in services — go through `errors`.
- Don't raise `HTTPException` or bare `Exception` — use typed errors.
- Don't put error-handling logic in error classes — that belongs in `handle_exception`.
