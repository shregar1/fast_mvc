# Middlewares

## What this module does

The **`middlewares`** package holds **application-specific** FastAPI/Starlette middleware **subclasses** and glue code. **Generic** middleware (CORS, rate limit, request ID, security headers, etc.) usually lives in **`fast-middleware`** / **`fastmiddleware`**; this folder is for behavior that **must** integrate with **this** app’s auth, repositories, or DTOs (e.g. JWT validation with your user store).

Middleware runs **around** every matching request: order of registration matters (outermost added first, depending on Starlette behavior).

## Overview

Generic HTTP middleware (request ID, security headers, rate limiting, CORS, timing, body-size limits, etc.) comes from **`fast-middleware`** on PyPI (`fastx_middleware` imports) and, in full templates, the extended **`fastmiddleware`** stack used in `app.py`.

This directory only contains **app-specific** wiring:

- **`authentication.py`** — Subclasses `JWTBearerAuthMiddleware` from `fastx_middleware`, binding JWT decode, user repository session checks, and `IResponseDTO` error payloads.

Import the app middleware as:

```python
from middlewares import AuthenticationMiddleware
```

Use the packaged stack in `app.py`, for example:

```python
from fastmiddleware import (
    CORSMiddleware,
    LoggingMiddleware,
    RateLimitMiddleware,
    RequestContextMiddleware,
    SecurityHeadersMiddleware,
    TimingMiddleware,
    TrustedHostMiddleware,
)

app.add_middleware(RequestContextMiddleware)
# ... trusted host, CORS, security headers, rate limit, logging, timing ...
app.add_middleware(AuthenticationMiddleware)
```

## Generic JWT middleware (library)

`JWTBearerAuthMiddleware` lives in **`fastx_middleware.jwt_bearer_auth`**. It takes injectable callables (`decode_bearer`, `load_user`, `build_error_response`, …) so other apps can reuse it without depending on FastX’s repositories or DTOs.

```python
from fastx_middleware import JWTBearerAuthMiddleware, ErrorKind
```

See the `fast-middleware` package README for `BodySizeLimitMiddleware`, `SecurityHeadersMiddleware`, `RequestIDMiddleware`, and related helpers.
