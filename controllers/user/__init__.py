"""User controllers – delegates to controllers.auth.user.

This package exists so that ``from controllers.user import router``
resolves for :mod:`app` and for the internal imports inside
``controllers/auth/user/*.py``.

The actual import is deferred to avoid a circular dependency:
``controllers.auth.user.__init__`` imports ``controllers.user.abstraction``
and sibling modules, so we must not trigger ``controllers.auth.user``
during our own init.
"""

from __future__ import annotations


def __getattr__(name: str):
    """Lazily expose ``router`` (and any other names) from controllers.auth.user."""
    if name == "router":
        from controllers.auth.user import router
        return router
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["router"]
