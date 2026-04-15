"""User Subscription Service."""

from __future__ import annotations

from typing import Any

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from services.user.abstraction import IUserService


class UserSubscriptionService(IUserService):
    """Returns the current user's active subscription."""

    def __init__(
        self,
        subscription_repository: Any = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.subscription_repository = subscription_repository

    async def run(self, request_dto: Any = None) -> BaseResponseDTO:
        """Alias for :meth:`get_current`."""
        return await self.get_current()

    async def get_current(self) -> BaseResponseDTO:
        """Get the current user's active subscription."""
        subscription = None
        if self.subscription_repository and self.user_id:
            try:
                subscription = self.subscription_repository.get_active_for_user(
                    user_id=self.user_id
                )
            except Exception:
                pass

        if subscription is None:
            return BaseResponseDTO(
                transactionUrn=self.urn or "",
                status=APIStatus.SUCCESS,
                responseMessage="No active subscription.",
                responseKey="success_no_subscription",
                data={"subscription": None},
            )

        sub_data = (
            subscription.to_dict()
            if hasattr(subscription, "to_dict")
            else {"id": getattr(subscription, "id", None)}
        )

        return BaseResponseDTO(
            transactionUrn=self.urn or "",
            status=APIStatus.SUCCESS,
            responseMessage="Subscription retrieved.",
            responseKey="success_get_subscription",
            data={"subscription": sub_data},
        )


__all__ = ["UserSubscriptionService"]
