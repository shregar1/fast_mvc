"""User service dependency abstraction."""

from __future__ import annotations

from dependencies.services.abstraction import IServiceDependency


class IUserAuthServiceDependency(IServiceDependency):
    """Interface for user-auth-scoped service dependencies."""

    pass


__all__ = ["IUserAuthServiceDependency"]
