"""Verify-MFA Service – exchanges MFA challenge token + code for full JWT."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import jwt

from constants.api_status import APIStatus
from dtos.requests.user.account.verify_mfa import VerifyMFARequestDTO
from dtos.responses.base import BaseResponseDTO
from fastx_platform.errors import BadInputError, UnauthorizedError
from repositories.user.user_repository import UserRepository
from services.user.abstraction import IUserService
from services.user.token_issuance import TokenIssuanceService
from start_utils import ALGORITHM, SECRET_KEY


class VerifyMFAService(IUserService):
    """Verify an MFA code against a challenge token and issue full JWTs."""

    def __init__(
        self,
        *args: Any,
        user_repository: UserRepository,
        mfa_service: Any,
        token_issuance_service: Optional[TokenIssuanceService] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._user_repository = user_repository
        self._mfa_service = mfa_service
        self._token_issuance_service = token_issuance_service

    async def run(self, request_dto: VerifyMFARequestDTO | None = None) -> BaseResponseDTO:
        try:
            payload = jwt.decode(
                request_dto.mfa_challenge_token, SECRET_KEY, algorithms=[ALGORITHM],
            )
        except Exception as err:
            raise UnauthorizedError(
                httpStatusCode=401,
                responseMessage="Invalid or expired MFA challenge token.",
                responseKey="error_authentication_error",
            ) from err
        if payload.get("purpose") != "mfa_challenge":
            raise UnauthorizedError(
                httpStatusCode=401,
                responseMessage="Invalid token.",
                responseKey="error_authentication_error",
            )

        user_id = payload.get("user_id")
        user_urn = payload.get("user_urn")
        user = self._user_repository.retrieve_record_by_id(user_id)
        if not user:
            raise UnauthorizedError(
                httpStatusCode=401,
                responseMessage="User not found.",
                responseKey="error_authentication_error",
            )

        secret = user.mfa_secret
        code_ok = bool(secret and self._mfa_service.verify_totp(secret, request_dto.code))
        if not code_ok:
            backup_hash = getattr(user, "mfa_backup_codes_hash", None) or ""
            matched, remaining = self._mfa_service.verify_backup_code(request_dto.code, backup_hash)
            if matched:
                user.mfa_backup_codes_hash = remaining
                code_ok = True
        if not code_ok:
            raise BadInputError(
                httpStatusCode=400,
                responseMessage="Invalid MFA code.",
                responseKey="error_bad_input",
            )

        user.is_logged_in = True
        user.last_login = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        # NOTE: commit is owned by the caller / UoW. Do not commit here.

        tokens = await self._token_issuance_service.issue(
            user_id=user.id,
            user_urn=user.urn,
            email=user.email,
            public_key_pem=getattr(user, "public_key_pem", None),
        )

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully logged in.",
            responseKey="success_user_login",
            data={"status": True, **tokens},
        )


__all__ = ["VerifyMFAService"]
