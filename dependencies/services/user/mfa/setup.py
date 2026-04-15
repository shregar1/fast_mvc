"""MFA Setup Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class MFASetupServiceDependency:
    """FastAPI dependency provider for MFASetupService."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating MFASetupService instances."""
        logger.debug("MFASetupServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
        ) -> Any:
            from services.user.mfa.setup import MFASetupService

            return MFASetupService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                session=session,
            )

        return factory


__all__ = ["MFASetupServiceDependency"]
