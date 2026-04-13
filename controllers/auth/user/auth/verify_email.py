"""GET /user/auth/verify-email?token=... – Verify account via link sent to email.

Also registered as **GET /user/verify-email** (same handler) for clients that use the `/user` prefix.
"""

import os
from datetime import datetime, timezone
from http import HTTPStatus

import jwt
from fastapi import Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_lk import APILK
from constants.api_status import APIStatus
from dependencies.db import DBDependency
from dtos.responses.base import BaseResponseDTO
from repositories.user.user_repository import UserRepository
from start_utils import ALGORITHM, SECRET_KEY
from controllers.apis.v1.abstraction import IV1APIController


class VerifyEmailController(IV1APIController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name=APILK.AUTH_VERIFY_EMAIL)

    async def get(
        self,
        request: Request,
        token: str = Query(..., description="Verification token from the email link."),
        session: Session = Depends(DBDependency.derive),
    ) -> JSONResponse:
        """
        Verify email using the token from the verification link.
        Decodes the JWT, checks purpose=email_verification, finds the user,
        sets email_verified_at, and returns success or error.
        """
        self.urn = getattr(request.state, "urn", "") or ""
        self.user_id = getattr(request.state, "user_id", None)
        self.user_urn = getattr(request.state, "user_urn", None)
        self.logger = self.logger.bind(
            urn=self.urn, user_urn=self.user_urn, api_name=self.api_name
        )

        async def _run() -> JSONResponse:
            response_dto = BaseResponseDTO(
                transactionUrn=getattr(request.state, "urn", "") or "",
                status=APIStatus.FAILED,
                responseMessage="Invalid or expired verification link.",
                responseKey="error_verify_email_invalid",
                data={},
            )
            status_code = HTTPStatus.BAD_REQUEST

            if not token or not token.strip():
                return JSONResponse(status_code=status_code, content=response_dto.model_dump())

            try:
                payload = jwt.decode(
                    token.strip(),
                    SECRET_KEY,
                    algorithms=[ALGORITHM],
                )
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                return JSONResponse(status_code=status_code, content=response_dto.model_dump())

            if payload.get("purpose") != "email_verification":
                return JSONResponse(status_code=status_code, content=response_dto.model_dump())

            email = payload.get("email")
            if not email:
                return JSONResponse(status_code=status_code, content=response_dto.model_dump())

            repo = UserRepository(
                urn=getattr(request.state, "urn", ""),
                user_urn=None,
                api_name="verify_email",
                session=session,
                user_id=None,
            )
            user = repo.retrieve_record_by_email(email, is_deleted=False)
            if not user:
                return JSONResponse(status_code=status_code, content=response_dto.model_dump())

            if getattr(user, "email_verified_at", None) is not None:
                response_dto = BaseResponseDTO(
                    transactionUrn=getattr(request.state, "urn", "") or "",
                    status=APIStatus.SUCCESS,
                    responseMessage="Email is already verified.",
                    responseKey="success_email_already_verified",
                    data={
                        "email_verified_at": user.email_verified_at.isoformat()
                        if user.email_verified_at
                        else None
                    },
                )
                return JSONResponse(status_code=HTTPStatus.OK, content=response_dto.model_dump())

            now = datetime.now(timezone.utc)
            user.email_verified_at = now
            session.commit()
            session.refresh(user)

            response_dto = BaseResponseDTO(
                transactionUrn=getattr(request.state, "urn", "") or "",
                status=APIStatus.SUCCESS,
                responseMessage="Email verified successfully.",
                responseKey="success_email_verified",
                data={"email_verified_at": now.isoformat()},
            )
            return JSONResponse(status_code=HTTPStatus.OK, content=response_dto.model_dump())

        return await self.invoke_with_exception_handling(request, _run)


__all__ = ["VerifyEmailController"]
