"""MFA QR-Code Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class MFAQrCodeServiceDependency:
    """FastAPI dependency provider for MFAQrCodeService."""

    @staticmethod
    def derive() -> Callable:
        """Return a factory for creating MFAQrCodeService instances."""
        logger.debug("MFAQrCodeServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
        ) -> Any:
            from services.user.mfa.qr_code import MFAQrCodeService

            return MFAQrCodeService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                session=session,
            )

        return factory


__all__ = ["MFAQrCodeServiceDependency"]
