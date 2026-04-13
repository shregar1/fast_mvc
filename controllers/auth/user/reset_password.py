"""
POST /user/reset-password – Confirm a password reset with token + new password.

Public (unauthenticated) endpoint. Validates the JWT reset token
(purpose=password_reset), hashes the new password, and updates the user record.
"""

import os
from http import HTTPStatus

import bcrypt
import jwt
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from structured_log import log_event
from dependencies.db import DBDependency
from dtos.requests.user.reset_password import ResetPasswordRequestDTO
from dtos.responses.base import BaseResponseDTO
from fast_database.persistence.models.user import User
from start_utils import ALGORITHM, SECRET_KEY


def _hash_password(password: str) -> str:
    """Hash password with BCRYPT_SALT or bcrypt.gensalt(). Matches registration flow."""
    salt = os.getenv("BCRYPT_SALT")
    if not salt:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    try:
        return bcrypt.hashpw(password.encode("utf-8"), salt.encode("utf-8")).decode("utf-8")
    except ValueError:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _error(urn: str, message: str, key: str = "error_bad_input") -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content=BaseResponseDTO(
            transactionUrn=urn,
            status=APIStatus.FAILED,
            responseMessage=message,
            responseKey=key,
            data={},
        ).model_dump(),
    )


async def reset_password(
    request: Request,
    body: ResetPasswordRequestDTO,
    session: Session = Depends(DBDependency.derive),
) -> JSONResponse:
    urn = getattr(request.state, "urn", "") or ""

    try:
        payload = jwt.decode(body.token.strip(), SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return _error(urn, "Invalid or expired reset token.")

    if payload.get("purpose") != "password_reset":
        return _error(urn, "Invalid reset token.")

    email = payload.get("email")
    if not email or not isinstance(email, str):
        return _error(urn, "Invalid reset token.")

    user = (
        session.query(User)
        .filter(User.email == email.strip().lower(), User.is_deleted.is_(False))
        .first()
    )
    if not user:
        return _error(urn, "Invalid or expired reset token.")

    user.password = _hash_password(body.new_password)
    session.commit()

    log_event("reset_password.success", urn=urn, email=email)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=BaseResponseDTO(
            transactionUrn=urn,
            status=APIStatus.SUCCESS,
            responseMessage="Password has been reset. You can log in with your new password.",
            responseKey="success_password_reset_confirm",
            data={},
        ).model_dump(),
    )
