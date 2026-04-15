"""MFA Status Service – report whether MFA is enabled for the current user."""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from fast_database.persistence.models.user import User
from fast_platform.errors import NotFoundError, UnauthorizedError
from start_utils import logger


class MFAStatusService:
    """Return the current user's MFA enablement flag."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Any = None,
        session: Optional[Session] = None,
    ) -> None:
        self._urn = urn or ""
        self._user_urn = user_urn
        self._api_name = api_name or "MFA_STATUS"
        self._user_id = user_id
        self._session = session
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

        return BaseResponseDTO(
            transactionUrn=self._urn,
            status=APIStatus.SUCCESS,
            responseMessage="Fetched MFA status.",
            responseKey="success_mfa_status",
            data={"enabled": bool(getattr(user, "mfa_enabled", False))},
        )


__all__ = ["MFAStatusService"]
