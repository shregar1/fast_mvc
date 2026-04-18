"""MFA Setup Service – start MFA enrollment for the current user."""

from __future__ import annotations

from typing import Any

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import BadInputError, NotFoundError, UnauthorizedError
from repositories.user.user_repository import UserRepository
from services.user.abstraction import IUserService


class MFASetupService(IUserService):
    """Generate a TOTP secret + provisioning URI for the authenticated user."""

    def __init__(
        self,
        *args: Any,
        user_repository: UserRepository,
        mfa_service: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._user_repository = user_repository
        self._mfa_service = mfa_service

    async def run(self, request_dto: Any = None) -> BaseResponseDTO:
        if self.user_id is None:
            raise UnauthorizedError(
                responseMessage="Unauthorized.",
                responseKey="error_authentication_error",
            )
        user = self._user_repository.retrieve_record_by_id(self.user_id)
        if not user:
            raise NotFoundError(
                responseMessage="User not found.",
                responseKey="error_user_not_found",
            )
        if user.mfa_enabled:
            raise BadInputError(
                responseMessage="MFA is already enabled.",
                responseKey="error_bad_input",
            )

        secret = self._mfa_service.generate_secret()
        self._user_repository.set_mfa_secret(user, secret)
        provisioning_uri = self._mfa_service.get_provisioning_uri(
            secret, user.email or "user",
        )

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Scan QR with authenticator app, then call verify to enable.",
            responseKey="success_mfa_setup",
            data={"secret": secret, "provisioningUri": provisioning_uri},
        )


__all__ = ["MFASetupService"]
