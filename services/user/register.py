"""User Registration Service."""

from __future__ import annotations

import os
from typing import Any
from uuid import uuid4

import bcrypt

from constants.api_status import APIStatus
from dtos.requests.user.registration import UserRegistrationRequestDTO
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import ConflictError
from services.user.abstraction import IUserService


class UserRegistrationService(IUserService):
    """Creates a new user account.

    Validates uniqueness, hashes password, persists user, and returns
    success response DTO.
    """

    def __init__(
        self,
        user_repository: Any = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.user_repository = user_repository

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash a password with bcrypt.

        Uses ``BCRYPT_SALT`` env var when set (deterministic hashing for
        test reproducibility).  Falls back to ``bcrypt.gensalt()`` in
        production.
        """
        salt_env = os.getenv("BCRYPT_SALT")
        if salt_env:
            try:
                salt = salt_env.encode("utf-8") if isinstance(salt_env, str) else salt_env
                return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
            except (ValueError, TypeError):
                pass
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    async def run(self, request_dto: UserRegistrationRequestDTO) -> BaseResponseDTO:
        """Register a new user."""
        existing = self.user_repository.retrieve_record_by_email(
            request_dto.email, is_deleted=False
        )
        if existing:
            raise ConflictError(
                responseMessage="An account with this email already exists.",
                responseKey="error_duplicate_email",
            )

        hashed = self._hash_password(request_dto.password)
        user = self.user_repository.create_record({
            "email": request_dto.email,
            "password": hashed,
            "urn": f"urn:user:{uuid4()}",
            "user_type_id": 1,
        })

        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)

        return BaseResponseDTO(
            transactionUrn=self.urn or "",
            status=APIStatus.SUCCESS,
            responseMessage="Registration successful.",
            responseKey="success_registration",
            data={
                "user_id": user_id,
                "user_email": request_dto.email,
            },
        )


__all__ = ["UserRegistrationService"]
