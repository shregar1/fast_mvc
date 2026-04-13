"""
POST /user/forgot-password – Request a password-reset email.

Public (unauthenticated) endpoint. If the email is registered, a JWT reset
link is sent. Always returns the same success response to prevent email
enumeration.
"""

import os
from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from constants.default import Default
from structured_log import log_event
from dependencies.db import DBDependency
from dtos.requests.user.forgot_password import ForgotPasswordRequestDTO
from dtos.responses.base import BaseResponseDTO
from repositories.user.user_repository import UserRepository
from utilities.notifications.lifecycle import send_password_reset_email
from start_utils import ALGORITHM, SECRET_KEY


async def forgot_password(
    request: Request,
    body: ForgotPasswordRequestDTO,
    session: Session = Depends(DBDependency.derive),
) -> JSONResponse:
    urn = getattr(request.state, "urn", "") or ""

    repo = UserRepository(
        urn=urn,
        user_urn=None,
        api_name="forgot_password",
        session=session,
        user_id=None,
    )
    user = repo.retrieve_record_by_email(body.email, is_deleted=False)

    if user:
        expires_minutes = Default.EMAIL_TOKEN_EXPIRY_MINUTES
        exp = datetime.utcnow() + timedelta(minutes=expires_minutes)
        token = jwt.encode(
            {"email": body.email, "exp": exp, "purpose": "password_reset"},
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
                body.email,
                reset_link,
                expires_minutes=expires_minutes,
            )
        except Exception:
            pass

        log_event("forgot_password.email_sent", urn=urn, email=body.email)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=BaseResponseDTO(
            transactionUrn=urn,
            status=APIStatus.SUCCESS,
            responseMessage="If that email is registered, you will receive a reset link.",
            responseKey="success_password_reset_request",
            data={},
        ).model_dump(),
    )
