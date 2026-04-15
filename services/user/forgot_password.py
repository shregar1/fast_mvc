"""Forgot-password service – issues a time-limited JWT reset link via email."""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from sqlalchemy.orm import Session

from constants.default import Default
from dtos.responses.base import BaseResponseDTO
from constants.api_status import APIStatus
from repositories.user.user_repository import UserRepository
from start_utils import ALGORITHM, SECRET_KEY, logger
from structured_log import log_event
from utilities.notifications.lifecycle import send_password_reset_email


class ForgotPasswordService:
    """Orchestrates the forgot-password flow."""

    def __init__(
        self,
        urn: Optional[str] = None,
        api_name: Optional[str] = None,
        session: Optional[Session] = None,
        user_repository: Optional[UserRepository] = None,
    ) -> None:
        self._urn = urn or ""
        self._api_name = api_name or "forgot_password"
        self._session = session
        self._repo = user_repository or UserRepository(
            urn=self._urn,
            user_urn=None,
            api_name=self._api_name,
            session=session,
            user_id=None,
        )
        self._logger = logger.bind(urn=self._urn, api_name=self._api_name)

    async def run(self, email: str) -> BaseResponseDTO:
        user = self._repo.retrieve_record_by_email(email, is_deleted=False)
        if user:
            expires_minutes = Default.EMAIL_TOKEN_EXPIRY_MINUTES
            exp = datetime.utcnow() + timedelta(minutes=expires_minutes)
            token = jwt.encode(
                {"email": email, "exp": exp, "purpose": "password_reset"},
                SECRET_KEY,
                algorithm=ALGORITHM,
            )
            if hasattr(token, "decode"):
                token = token.decode(Default.ENCODING_UTF8)

            base_url = os.getenv(
                "APP_URL", os.getenv("FRONTEND_URL", "https://app.example.com")
            ).rstrip("/")
            reset_link = f"{base_url}/reset-password?token={token}"

            try:
                await send_password_reset_email(
                    email, reset_link, expires_minutes=expires_minutes,
                )
            except Exception as err:
                self._logger.warning("Password reset email send failed: %s", err)

            log_event("forgot_password.email_sent", urn=self._urn, email=email)

        return BaseResponseDTO(
            transactionUrn=self._urn,
            status=APIStatus.SUCCESS,
            responseMessage="If that email is registered, you will receive a reset link.",
            responseKey="success_password_reset_request",
            data={},
        )


__all__ = ["ForgotPasswordService"]
