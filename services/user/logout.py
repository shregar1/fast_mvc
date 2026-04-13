"""User Logout Service."""

from __future__ import annotations

from typing import Any, Optional

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from services.user.abstraction import IUserService
from start_utils import logger


class UserLogoutService(IUserService):
    """Terminates a user session and invalidates tokens."""

    def __init__(
        self,
        user_repository: Any = None,
        jwt_utility: Any = None,
        refresh_token_repository: Any = None,
        auth_token: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.user_repository = user_repository
        self.jwt_utility = jwt_utility
        self.refresh_token_repository = refresh_token_repository
        self.auth_token = auth_token

    async def run(self, request_dto: Any = None) -> BaseResponseDTO:
        """Logout user — revoke tokens and clear login state."""
        # Invalidate refresh tokens for the user
        if self.user_id and self.refresh_token_repository:
            try:
                self.refresh_token_repository.revoke_all(user_id=self.user_id)
            except Exception as exc:
                logger.warning("Failed to revoke refresh tokens for user %s: %s", self.user_id, exc)

        # Update login state
        if self.user_id and self.user_repository:
            try:
                user = self.user_repository.retrieve_record_by_id(self.user_id)
                if user and hasattr(user, "last_login"):
                    user.last_login = None
            except Exception as exc:
                logger.warning("Failed to update login state for user %s: %s", self.user_id, exc)

        return BaseResponseDTO(
            transactionUrn=self.urn or "",
            status=APIStatus.SUCCESS,
            responseMessage="Logout successful.",
            responseKey="success_logout",
            data={},
        )


__all__ = ["UserLogoutService"]
