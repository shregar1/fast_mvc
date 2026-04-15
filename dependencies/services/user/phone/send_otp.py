"""Phone Send-OTP Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class PhoneSendOtpServiceDependency:
    """FastAPI dependency provider for PhoneSendOtpService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("PhoneSendOtpServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
            redis_client: Any = None,
        ) -> Any:
            from services.user.phone.send_otp import PhoneSendOtpService

            return PhoneSendOtpService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                session=session,
                redis_client=redis_client,
            )

        return factory


__all__ = ["PhoneSendOtpServiceDependency"]
