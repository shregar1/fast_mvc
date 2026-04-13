"""POST /user/mfa/disable – Disable MFA (requires current TOTP or backup code)."""

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


class MFADisableRequestDTO(BaseModel):
    code: str


class MFADisableController(IV1APIController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name=APILK.MFA_DISABLE)

    async def post(
        self,
        request: Request,
        body: MFADisableRequestDTO,
        session: Session = Depends(DBDependency.derive),
    ) -> JSONResponse:
        """
        POST /user/mfa/disable – Disable MFA (requires current TOTP or backup code).
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

            if not getattr(user, "mfa_enabled", False):
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", ""),
                        status=APIStatus.FAILED,
                        responseMessage="MFA is not enabled.",
                        responseKey="error_bad_input",
                        data={},
                    ).model_dump(),
                )

            code_ok = False
            secret = getattr(user, "mfa_secret", None)
            mfa_svc = MFAService(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=int(user_id),
            )
            if secret and mfa_svc.verify_totp(secret, body.code):
                code_ok = True

            if not code_ok and mfa_svc.consume_backup_code(session, user_id, body.code):
                code_ok = True

            if not code_ok:
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

            user.mfa_enabled = False
            user.mfa_secret = None
            user.mfa_backup_codes_hash = None
            session.commit()
            log_audit(
                session,
                "mfa.disabled",
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
                    responseMessage="MFA disabled.",
                    responseKey="success_mfa_disabled",
                    data={"enabled": False},
                ).model_dump(),
            )
        except Exception as err:
            return self._handle_controller_exception(request=request, err=err)


__all__ = ["MFADisableRequestDTO", "MFADisableController"]
