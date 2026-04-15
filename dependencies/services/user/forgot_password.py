"""Forgot-Password Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class ForgotPasswordServiceDependency:
    """FastAPI dependency provider for ForgotPasswordService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("ForgotPasswordServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
        ) -> Any:
            from services.user.forgot_password import ForgotPasswordService

            return ForgotPasswordService(
                urn=urn,
                api_name=api_name,
                session=session,
            )

        return factory


__all__ = ["ForgotPasswordServiceDependency"]
