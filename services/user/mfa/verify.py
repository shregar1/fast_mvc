"""MFA Verify Service – verify TOTP code and enable MFA."""

from __future__ import annotations

from typing import Any

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from fastx_platform.errors import BadInputError, NotFoundError, UnauthorizedError
from repositories.user.user_repository import UserRepository
from services.user.abstraction import IUserService
from utilities.audit import log_audit


class MFAVerifyService(IUserService):
    """Verify a TOTP code against the pending secret and enable MFA."""

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
                httpStatusCode=401,
                responseMessage="Unauthorized.",
                responseKey="error_authentication_error",
            )
        user = self._user_repository.retrieve_record_by_id(self.user_id)
        if not user:
            raise NotFoundError(
                httpStatusCode=404,
                responseMessage="User not found.",
                responseKey="error_user_not_found",
            )

        secret = user.mfa_secret
        if not secret:
            raise BadInputError(
                httpStatusCode=400,
                responseMessage="Call setup first.",
                responseKey="error_bad_input",
            )
        if not self._mfa_service.verify_totp(secret, request_dto):
            raise BadInputError(
                httpStatusCode=400,
                responseMessage="Invalid code.",
                responseKey="error_bad_input",
            )

        backup_codes = self._mfa_service.generate_backup_codes()
        self._user_repository.set_mfa_enabled(user, True)
        user.mfa_backup_codes_hash = self._mfa_service.hash_backup_codes(backup_codes)
        log_audit(
            self._user_repository.session,
            "mfa.enabled",
            "user",
            actor_id=int(self.user_id),
            actor_urn=getattr(user, "urn", None),
            resource_id=str(user.id),
        )

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="MFA enabled. Store backup codes securely; they will not be shown again.",
            responseKey="success_mfa_enabled",
            data={"enabled": True, "backupCodes": backup_codes},
        )


__all__ = ["MFAVerifyService"]
