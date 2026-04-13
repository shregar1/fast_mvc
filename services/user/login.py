"""User Login Service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import bcrypt

from constants.api_status import APIStatus
from constants.default import Default
from dtos.requests.user.login import UserLoginRequestDTO
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import (
    NotFoundError,
    UnauthorizedError,
)
from services.user.abstraction import IUserService
from start_utils import logger


class UserLoginService(IUserService):
    """Authenticates a user by email/password and returns tokens.

    If the user has MFA enabled, returns an MFA challenge token instead
    of full access/refresh tokens.
    """

    def __init__(
        self,
        user_repository: Any = None,
        jwt_utility: Any = None,
        refresh_token_repository: Any = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.user_repository = user_repository
        self.jwt_utility = jwt_utility
        self.refresh_token_repository = refresh_token_repository

    async def run(self, request_dto: UserLoginRequestDTO) -> BaseResponseDTO:
        """Authenticate user and return token response DTO."""
        user = self.user_repository.retrieve_record_by_email(
            request_dto.email, is_deleted=False
        )
        if not user:
            raise NotFoundError(
                responseMessage="Invalid email or password.",
                responseKey="error_invalid_credentials",
                httpStatusCode=404,
            )

        stored_hash = user.password
        if not isinstance(stored_hash, bytes):
            stored_hash = stored_hash.encode("utf-8")

        if not bcrypt.checkpw(
            request_dto.password.encode("utf-8"),
            stored_hash,
        ):
            raise UnauthorizedError(
                responseMessage="Invalid email or password.",
                responseKey="error_invalid_credentials",
            )

        user_urn = getattr(user, "urn", None) or ""
        user_id = user.id

        # MFA flow
        if getattr(user, "mfa_enabled", False):
            mfa_token = self.jwt_utility.generate_token(
                {"user_id": user_id, "email": user.email, "purpose": "mfa_challenge"},
                expires_minutes=Default.MFA_TOKEN_EXPIRY_MINUTES,
            )
            public_key_pem = getattr(user, "public_key_pem", None)
            data: dict[str, Any] = {
                "requiresMFA": True,
                "mfaChallengeToken": mfa_token,
                "userUrn": user_urn,
            }
            if public_key_pem:
                data["publicKeyPem"] = public_key_pem
            return BaseResponseDTO(
                transactionUrn=self.urn or "",
                status=APIStatus.SUCCESS,
                responseMessage="MFA verification required.",
                responseKey="success_mfa_required",
                data=data,
            )

        # Standard token flow
        token_payload = {
            "user_id": user_id,
            "email": user.email,
            "user_urn": user_urn,
        }
        access_token = self.jwt_utility.generate_token(token_payload)
        refresh_token = self.jwt_utility.generate_refresh_token(token_payload)

        # Persist refresh token
        if self.refresh_token_repository:
            try:
                self.refresh_token_repository.store(
                    user_id=user_id,
                    token=refresh_token,
                )
            except Exception as exc:
                logger.warning("Failed to persist refresh token for user %s: %s", user_id, exc)

        # Update login state on the model (will be committed by controller/session)
        try:
            if hasattr(user, "last_login"):
                user.last_login = datetime.now(timezone.utc)
        except Exception:
            pass

        public_key_pem = getattr(user, "public_key_pem", None)
        data = {
            "status": True,
            "token": access_token,
            "refreshToken": refresh_token,
            "userUrn": user_urn,
            "userId": user_id,
            "user_id": user_id,
            "user_urn": user_urn,
        }
        if public_key_pem:
            data["publicKeyPem"] = public_key_pem

        return BaseResponseDTO(
            transactionUrn=self.urn or "",
            status=APIStatus.SUCCESS,
            responseMessage="Successfully logged in the user.",
            responseKey="success_user_login",
            data=data,
        )


__all__ = ["UserLoginService"]
