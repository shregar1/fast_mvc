"""MFA Status Service – report whether MFA is enabled for the current user."""

from __future__ import annotations

from typing import Any

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from fastx_platform.errors import NotFoundError, UnauthorizedError
from repositories.user.user_repository import UserRepository
from services.user.abstraction import IUserService


class MFAStatusService(IUserService):
    """Return the current user's MFA enablement flag."""

    def __init__(
        self,
        user_repository: UserRepository,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._user_repository = user_repository

    async def run(self, request_dto: Any = None) -> BaseResponseDTO:
        """Fetch MFA enablement flag for the authenticated user."""
        if self.user_id is None:
            raise UnauthorizedError(
                httpStatusCode=401,
                responseMessage="Unauthorized.",
                responseKey="error_authentication_error",
            )

        user = self._user_repository.retrieve_record_by_id(self.user_id)
        if user is None:
            raise NotFoundError(
                httpStatusCode=404,
                responseMessage="User not found.",
                responseKey="error_user_not_found",
            )

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Fetched MFA status.",
            responseKey="success_mfa_status",
            data={"enabled": bool(getattr(user, "mfa_enabled", False))},
        )


__all__ = ["MFAStatusService"]
