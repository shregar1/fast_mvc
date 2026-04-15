"""MFA Setup Service – start MFA enrollment for the current user."""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from fast_database.persistence.models.user import User
from fast_platform.errors import BadInputError, NotFoundError, UnauthorizedError
from services.mfa import MFAService
from start_utils import logger


class MFASetupService:
    """Generate a TOTP secret + provisioning URI for the authenticated user."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Any = None,
        session: Optional[Session] = None,
        mfa_service: Optional[MFAService] = None,
    ) -> None:
        self._urn = urn or ""
        self._user_urn = user_urn
        self._api_name = api_name or "MFA_SETUP"
        self._user_id = user_id
        self._session = session
        self._mfa = mfa_service or MFAService(
            urn=urn, user_urn=user_urn, api_name=api_name,
            user_id=int(user_id) if user_id else None,
        )
        self._logger = logger.bind(urn=self._urn, api_name=self._api_name)

    async def run(self) -> BaseResponseDTO:
        if not self._user_id:
            raise UnauthorizedError(
                responseMessage="Unauthorized.",
                responseKey="error_authentication_error",
            )
        user = self._session.query(User).filter(User.id == self._user_id).first()
        if not user:
            raise NotFoundError(
                responseMessage="User not found.",
                responseKey="error_user_not_found",
            )
        if getattr(user, "mfa_enabled", False):
            raise BadInputError(
                responseMessage="MFA is already enabled.",
                responseKey="error_bad_input",
            )

        secret = self._mfa.generate_secret()
        user.mfa_secret = secret
        self._session.commit()
        provisioning_uri = self._mfa.get_provisioning_uri(
            secret, user.email or "user",
        )

        return BaseResponseDTO(
            transactionUrn=self._urn,
            status=APIStatus.SUCCESS,
            responseMessage="Scan QR with authenticator app, then call verify to enable.",
            responseKey="success_mfa_setup",
            data={"secret": secret, "provisioningUri": provisioning_uri},
        )


__all__ = ["MFASetupService"]
