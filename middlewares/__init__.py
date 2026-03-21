"""
Middleware package.

Exports app-specific JWT authentication wired to ``fastmvc_middleware``.

Generic HTTP middleware (security headers, body limits, CORS, timing, etc.) lives in
the ``fastmvc-middleware`` distribution (import ``fastmvc_middleware`` or ``fastmiddleware``
depending on your stack). This package only provides :class:`AuthenticationMiddleware`.

Use::

    from middlewares import AuthenticationMiddleware
"""

from .authentication import AuthenticationMiddleware

__all__ = [
    "AuthenticationMiddleware",
]
