"""Verify-MFA Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class VerifyMFAServiceDependency:
    """FastAPI dependency provider for VerifyMFAService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("VerifyMFAServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
        ) -> Any:
            from services.user.account.verify_mfa import VerifyMFAService

            return VerifyMFAService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                session=session,
            )

        return factory


__all__ = ["VerifyMFAServiceDependency"]
