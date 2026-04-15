"""Reset-Password Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class ResetPasswordServiceDependency:
    """FastAPI dependency provider for ResetPasswordService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("ResetPasswordServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
        ) -> Any:
            from services.user.reset_password import ResetPasswordService

            return ResetPasswordService(
                urn=urn,
                api_name=api_name,
                session=session,
            )

        return factory


__all__ = ["ResetPasswordServiceDependency"]
