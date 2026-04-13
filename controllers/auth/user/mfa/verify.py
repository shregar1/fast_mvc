"""POST /user/mfa/verify – Verify TOTP code and enable MFA (returns backup codes once)."""

from http import HTTPStatus

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dependencies.db import DBDependency
from dtos.responses.base import BaseResponseDTO
from fast_database.persistence.models.user import User
from utilities.audit import log_audit
from services.mfa import MFAService
from controllers.apis.v1.abstraction import IV1APIController
from constants.api_lk import APILK


class MFAVerifyRequestDTO(BaseModel):
    code: str


class MFAVerifyController(IV1APIController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name=APILK.MFA_VERIFY)

    async def post(
        self,
        request: Request,
        body: MFAVerifyRequestDTO,
        session: Session = Depends(DBDependency.derive),
    ) -> JSONResponse:
        """
        POST /user/mfa/verify – Verify TOTP code and enable MFA.
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
                return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={})

            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={})

            secret = getattr(user, "mfa_secret", None)
            if not secret:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", ""),
                        status=APIStatus.FAILED,
                        responseMessage="Call setup first.",
                        responseKey="error_bad_input",
                        data={},
                    ).model_dump(),
                )

            mfa_svc = MFAService(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=int(user_id),
            )
            if not mfa_svc.verify_totp(secret, body.code):
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", ""),
                        status=APIStatus.FAILED,
                        responseMessage="Invalid code.",
                        responseKey="error_bad_input",
                        data={},
                    ).model_dump(),
                )

            backup_codes = mfa_svc.generate_backup_codes()
            user.mfa_enabled = True
            user.mfa_backup_codes_hash = mfa_svc.hash_backup_codes(backup_codes)
            session.commit()
            log_audit(
                session,
                "mfa.enabled",
                "user",
                actor_id=int(user_id),
                actor_urn=getattr(user, "urn", None),
                resource_id=str(user.id),
            )

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=BaseResponseDTO(
                    transactionUrn=getattr(request.state, "urn", "") or "",
                    status=APIStatus.SUCCESS,
                    responseMessage="MFA enabled. Store backup codes securely; they will not be shown again.",
                    responseKey="success_mfa_enabled",
                    data={"enabled": True, "backupCodes": backup_codes},
                ).model_dump(),
            )
        except Exception as err:
            return self._handle_controller_exception(request=request, err=err)


__all__ = ["MFAVerifyRequestDTO", "MFAVerifyController"]
