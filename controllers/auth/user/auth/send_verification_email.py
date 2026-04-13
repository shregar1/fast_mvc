"""POST /user/auth/send-verification-email – Send verification link to current user's email."""

import os
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import jwt
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_lk import APILK
from constants.api_status import APIStatus
from constants.default import Default
from dependencies.db import DBDependency
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import UnauthorizedError
from repositories.user.user_repository import UserRepository
from utilities.notifications.lifecycle import send_verify_email
from start_utils import ALGORITHM, SECRET_KEY
from controllers.apis.v1.abstraction import IV1APIController


class SendVerificationEmailController(IV1APIController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name=APILK.AUTH_SEND_VERIFICATION_EMAIL)

    async def post(
        self,
        request: Request,
        session: Session = Depends(DBDependency.derive),
    ) -> JSONResponse:
        """
        Send account verification link to the authenticated user's email.
        Requires a valid JWT or API key (user_id in request.state).
        """
        self.urn = getattr(request.state, "urn", "") or ""
        self.user_id = getattr(request.state, "user_id", None)
        self.user_urn = getattr(request.state, "user_urn", None)
        self.logger = self.logger.bind(
            urn=self.urn, user_urn=self.user_urn, api_name=self.api_name
        )

        try:
            user_id = getattr(request.state, "user_id", None)
            if not user_id:
                raise UnauthorizedError(
                    responseMessage="Authentication required to send verification email.",
                    responseKey="error_unauthorized",
                )

            repo = UserRepository(
                urn=getattr(request.state, "urn", ""),
                user_urn=getattr(request.state, "user_urn", None),
                api_name="send_verification_email",
                session=session,
                user_id=str(user_id),
            )
            user = repo.retrieve_record_by_id(str(user_id))
            if not user or getattr(user, "is_deleted", False):
                raise UnauthorizedError(
                    responseMessage="User not found.",
                    responseKey="error_unauthorized",
                )

            email = getattr(user, "email", None)
            if not email:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", "") or "",
                        status=APIStatus.FAILED,
                        responseMessage="No email on account.",
                        responseKey="error_no_email",
                        data={},
                    ).model_dump(),
                )

            if getattr(user, "email_verified_at", None) is not None:
                return JSONResponse(
                    status_code=HTTPStatus.OK,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", "") or "",
                        status=APIStatus.SUCCESS,
                        responseMessage="Email is already verified.",
                        responseKey="success_email_already_verified",
                        data={},
                    ).model_dump(),
                )

            expires_minutes = Default.EMAIL_TOKEN_EXPIRY_MINUTES
            exp = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
            token = jwt.encode(
                {
                    "email": email,
                    "user_id": int(user_id),
                    "exp": exp,
                    "purpose": "email_verification",
                },
                SECRET_KEY,
                algorithm=ALGORITHM,
            )
            if hasattr(token, "decode"):
                token = token.decode(Default.ENCODING_UTF8)

            base_url = os.getenv("APP_URL", os.getenv("FRONTEND_URL", "https://app.example.com")).rstrip(
                "/"
            )
            verify_path = os.getenv("EMAIL_VERIFY_PATH", "/user/verify-email").strip() or "/user/verify-email"
            if not verify_path.startswith("/"):
                verify_path = "/" + verify_path
            verify_link = f"{base_url}{verify_path}?token={token}"

            try:
                await send_verify_email(
                    email,
                    verify_link,
                    expires_minutes=expires_minutes,
                )
            except Exception:
                return JSONResponse(
                    status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", "") or "",
                        status=APIStatus.FAILED,
                        responseMessage="Failed to send verification email. Please try again later.",
                        responseKey="error_send_failed",
                        data={},
                    ).model_dump(),
                )

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=BaseResponseDTO(
                    transactionUrn=getattr(request.state, "urn", "") or "",
                    status=APIStatus.SUCCESS,
                    responseMessage="Verification link sent to your email.",
                    responseKey="success_verification_email_sent",
                    data={},
                ).model_dump(),
            )
        except Exception as err:
            return self._handle_controller_exception(err, urn=getattr(request.state, "urn", "") or "")


__all__ = ["SendVerificationEmailController"]
