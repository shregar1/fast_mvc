"""Send-Verification-Email Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class SendVerificationEmailServiceDependency:
    """FastAPI dependency provider for SendVerificationEmailService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("SendVerificationEmailServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
        ) -> Any:
            from services.user.account.send_verification_email import (
                SendVerificationEmailService,
            )

            return SendVerificationEmailService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                session=session,
            )

        return factory


__all__ = ["SendVerificationEmailServiceDependency"]
