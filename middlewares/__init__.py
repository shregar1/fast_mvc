"""Middleware package.

Exports app-specific JWT authentication wired to ``fast_middleware``.

Generic HTTP middleware (security headers, body limits, CORS, timing, etc.) lives in
the ``fast-middleware`` distribution (import ``fast_middleware`` or ``fastmiddleware``
depending on your stack). This package only provides :class:`AuthenticationMiddleware`.

Use::

    from middlewares import AuthenticationMiddleware, DocsAuthConfig

OpenAPI path helpers (``normalized_openapi_url``, logging excludes, auth configured) live on
:class:`DocsAuthConfig` in :mod:`middlewares.docs_auth`.
"""

from .docs_auth import DocsAuthConfig, DocsBasicAuthMiddleware


__all__ = [
    "DocsAuthConfig",
    "DocsBasicAuthMiddleware",
]
