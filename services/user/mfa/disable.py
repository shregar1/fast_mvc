"""MFA Disable Service – turn off MFA after validating current code."""

from __future__ import annotations

from typing import Any

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import BadInputError, NotFoundError, UnauthorizedError
from repositories.user.user_repository import UserRepository
from services.user.abstraction import IUserService
from utilities.audit import log_audit


class MFADisableService(IUserService):
    """Disable MFA after verifying either a current TOTP or a backup code."""

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
        if not user.mfa_enabled:
            raise BadInputError(
                responseMessage="MFA is not enabled.",
                responseKey="error_bad_input",
            )

        secret = user.mfa_secret
        code_ok = bool(secret and self._mfa_service.verify_totp(secret, request_dto))

        if not code_ok:
            backup_hash = getattr(user, "mfa_backup_codes_hash", None) or ""
            matched, remaining = self._mfa_service.verify_backup_code(request_dto, backup_hash)
            if matched:
                user.mfa_backup_codes_hash = remaining
                code_ok = True

        if not code_ok:
            raise BadInputError(
                responseMessage="Invalid code.",
                responseKey="error_bad_input",
            )

        self._user_repository.set_mfa_enabled(user, False)
        self._user_repository.set_mfa_secret(user, None)
        user.mfa_backup_codes_hash = None
        log_audit(
            self._user_repository.session,
            "mfa.disabled",
            "user",
            actor_id=int(self.user_id),
            actor_urn=getattr(user, "urn", None),
            resource_id=str(user.id),
        )

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="MFA disabled.",
            responseKey="success_mfa_disabled",
            data={"enabled": False},
        )


__all__ = ["MFADisableService"]
