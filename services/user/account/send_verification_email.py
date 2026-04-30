"""Send-Verification-Email Service – mints a JWT link and dispatches it."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import jwt
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from constants.default import Default
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import (
    BadInputError,
    ServiceUnavailableError,
    UnauthorizedError,
)
from repositories.user.user_repository import UserRepository
from start_utils import ALGORITHM, SECRET_KEY, logger
from utilities.notifications.lifecycle import send_verify_email


class SendVerificationEmailService:
    """Generate a verification link and email it to the authenticated user."""

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
        self._api_name = api_name or "AUTH_SEND_VERIFICATION_EMAIL"
        self._user_id = user_id
        self._session = session
        self._logger = logger.bind(urn=self._urn, api_name=self._api_name)

    async def run(self) -> BaseResponseDTO:
        if not self._user_id:
            raise UnauthorizedError(
                httpStatusCode=401,
                responseMessage="Authentication required to send verification email.",
                responseKey="error_unauthorized",
            )
        repo = UserRepository(
            urn=self._urn,
            user_urn=self._user_urn,
            api_name=self._api_name,
            session=self._session,
            user_id=str(self._user_id),
        )
        user = repo.retrieve_record_by_id(str(self._user_id))
        if not user or getattr(user, "is_deleted", False):
            raise UnauthorizedError(
                httpStatusCode=401,
                responseMessage="User not found.",
                responseKey="error_unauthorized",
            )

        email = getattr(user, "email", None)
        if not email:
            raise BadInputError(
                httpStatusCode=400,
                responseMessage="No email on account.",
                responseKey="error_no_email",
            )
        if getattr(user, "email_verified_at", None) is not None:
            return BaseResponseDTO(
                transactionUrn=self._urn,
                status=APIStatus.SUCCESS,
                responseMessage="Email is already verified.",
                responseKey="success_email_already_verified",
                data={},
            )

        expires_minutes = Default.EMAIL_TOKEN_EXPIRY_MINUTES
        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        token = jwt.encode(
            {
                "email": email,
                "user_id": int(self._user_id),
                "exp": exp,
                "purpose": "email_verification",
            },
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
        if hasattr(token, "decode"):
            token = token.decode(Default.ENCODING_UTF8)

        base_url = os.getenv(
            "APP_URL", os.getenv("FRONTEND_URL", "https://app.example.com"),
        ).rstrip("/")
        verify_path = (
            os.getenv("EMAIL_VERIFY_PATH", "/user/verify-email").strip()
            or "/user/verify-email"
        )
        if not verify_path.startswith("/"):
            verify_path = "/" + verify_path
        verify_link = f"{base_url}{verify_path}?token={token}"

        try:
            await send_verify_email(
                email, verify_link, expires_minutes=expires_minutes,
            )
        except Exception as err:
            raise ServiceUnavailableError(
                httpStatusCode=503,
                responseMessage="Failed to send verification email. Please try again later.",
                responseKey="error_send_failed",
            ) from err

        return BaseResponseDTO(
            transactionUrn=self._urn,
            status=APIStatus.SUCCESS,
            responseMessage="Verification link sent to your email.",
            responseKey="success_verification_email_sent",
            data={},
        )


__all__ = ["SendVerificationEmailService"]
