"""Phone Verify-OTP Service Dependency."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from start_utils import logger


class PhoneVerifyOtpServiceDependency:
    """FastAPI dependency provider for PhoneVerifyOtpService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("PhoneVerifyOtpServiceDependency factory created")

        def factory(
            urn: str | None = None,
            user_urn: str | None = None,
            api_name: str | None = None,
            user_id: Any = None,
            session: Any = None,
            redis_client: Any = None,
            user_repository: Any = None,
            jwt_utility: Any = None,
            refresh_token_repository: Any = None,
        ) -> Any:
            from services.user.phone.verify_otp import PhoneVerifyOtpService

            return PhoneVerifyOtpService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                session=session,
                redis_client=redis_client,
                user_repository=user_repository,
                jwt_utility=jwt_utility,
                refresh_token_repository=refresh_token_repository,
            )

        return factory


__all__ = ["PhoneVerifyOtpServiceDependency"]
