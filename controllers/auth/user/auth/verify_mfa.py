"""POST /user/auth/verify-mfa – Verify MFA code and return full JWT. Public (uses mfa_challenge_token)."""

import uuid
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import jwt
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from constants.api_lk import APILK
from constants.api_status import APIStatus
from dependencies.db import DBDependency
from dtos.responses.base import BaseResponseDTO
from fast_database.persistence.models.user import User
from repositories.user.refresh_token_repository import RefreshTokenRepository
from start_utils import ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY
from controllers.apis.v1.abstraction import IV1APIController
from utilities.jwt import JWTUtility
from services.mfa import MFAService


class VerifyMFARequestDTO(BaseModel):
    mfa_challenge_token: str
    code: str


class VerifyMFAController(IV1APIController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name=APILK.AUTH_VERIFY_MFA)

    async def post(
        self,
        request: Request,
        body: VerifyMFARequestDTO,
        session: Session = Depends(DBDependency.derive),
    ) -> JSONResponse:
        """
        Exchange MFA challenge token + TOTP/backup code for full JWT.
        Call after login returns requiresMFA and mfaChallengeToken.
        """
        self.urn = getattr(request.state, "urn", "") or ""
        self.user_id = getattr(request.state, "user_id", None)
        self.user_urn = getattr(request.state, "user_urn", None)
        self.logger = self.logger.bind(
            urn=self.urn, user_urn=self.user_urn, api_name=self.api_name
        )

        try:
            urn = getattr(request.state, "urn", "") or ""
            try:
                payload = jwt.decode(
                    body.mfa_challenge_token,
                    SECRET_KEY,
                    algorithms=[ALGORITHM],
                )
            except Exception:
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content=BaseResponseDTO(
                        transactionUrn=urn,
                        status=APIStatus.FAILED,
                        responseMessage="Invalid or expired MFA challenge token.",
                        responseKey="error_authentication_error",
                        data={},
                    ).model_dump(),
                )

            if payload.get("purpose") != "mfa_challenge":
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content=BaseResponseDTO(
                        transactionUrn=urn,
                        status=APIStatus.FAILED,
                        responseMessage="Invalid token.",
                        responseKey="error_authentication_error",
                        data={},
                    ).model_dump(),
                )

            user_id = payload.get("user_id")
            user_urn = payload.get("user_urn")
            user = session.query(User).filter(User.id == user_id, User.is_deleted.is_(False)).first()
            if not user:
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content=BaseResponseDTO(
                        transactionUrn=urn,
                        status=APIStatus.FAILED,
                        responseMessage="User not found.",
                        responseKey="error_authentication_error",
                        data={},
                    ).model_dump(),
                )

            secret = getattr(user, "mfa_secret", None)
            code_ok = False
            mfa_svc = MFAService(urn=urn, user_urn=user_urn, api_name=self.api_name, user_id=int(user_id))
            if secret and mfa_svc.verify_totp(secret, body.code):
                code_ok = True

            if not code_ok and mfa_svc.consume_backup_code(session, user_id, body.code):
                code_ok = True

            if not code_ok:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content=BaseResponseDTO(
                        transactionUrn=urn,
                        status=APIStatus.FAILED,
                        responseMessage="Invalid MFA code.",
                        responseKey="error_bad_input",
                        data={},
                    ).model_dump(),
                )

            user.is_logged_in = True
            user.last_login = datetime.utcnow()
            user.updated_at = datetime.utcnow()
            session.commit()
            jwt_utility = JWTUtility(urn=urn, user_urn=user_urn, user_id=str(user_id))
            jti = str(uuid.uuid4())
            family_id = str(uuid.uuid4())
            try:
                days = int(REFRESH_TOKEN_EXPIRE_DAYS) if REFRESH_TOKEN_EXPIRE_DAYS is not None else 7
            except (TypeError, ValueError):
                days = 7
            expires_at = datetime.now(timezone.utc) + timedelta(days=days)
            payload_data = {
                "user_id": user.id,
                "user_urn": user.urn,
                "user_email": user.email,
                "last_login": str(user.last_login),
                "jti": jti,
                "family_id": family_id,
            }
            token = jwt_utility.create_access_token(data=payload_data)
            refresh_token = jwt_utility.create_refresh_token(data=payload_data)
            refresh_repo = RefreshTokenRepository(session=session)
            refresh_repo.create(jti=jti, user_id=user.id, family_id=family_id, expires_at=expires_at)

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=BaseResponseDTO(
                    transactionUrn=urn,
                    status=APIStatus.SUCCESS,
                    responseMessage="Successfully logged in.",
                    responseKey="success_user_login",
                    data={
                        "status": True,
                        "token": token,
                        "refreshToken": refresh_token,
                        "user_urn": user.urn,
                        "user_id": user.id,
                        "public_key_pem": getattr(user, "public_key_pem", None),
                    },
                ).model_dump(),
            )
        except Exception as err:
            return self._handle_controller_exception(request=request, err=err)


__all__ = ["VerifyMFARequestDTO", "VerifyMFAController"]
