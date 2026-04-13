"""POST /user/mfa/setup – Start MFA setup (returns secret + provisioning URI for QR)."""

from http import HTTPStatus

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dependencies.db import DBDependency
from dtos.responses.base import BaseResponseDTO
from fast_database.persistence.models.user import User
from services.mfa import MFAService
from controllers.apis.v1.abstraction import IV1APIController
from constants.api_lk import APILK


class MFASetupController(IV1APIController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name=APILK.MFA_SETUP)

    async def post(
        self,
        request: Request,
        session: Session = Depends(DBDependency.derive),
    ) -> JSONResponse:
        """
        POST /user/mfa/setup – Start MFA setup (returns secret + provisioning URI).
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
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", ""),
                        status=APIStatus.FAILED,
                        responseMessage="Unauthorized.",
                        responseKey="error_authentication_error",
                        data={},
                    ).model_dump(),
                )

            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={})

            if getattr(user, "mfa_enabled", False):
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", ""),
                        status=APIStatus.FAILED,
                        responseMessage="MFA is already enabled.",
                        responseKey="error_bad_input",
                        data={},
                    ).model_dump(),
                )

            mfa_svc = MFAService()
            secret = mfa_svc.generate_secret()
            user.mfa_secret = secret
            session.commit()
            provisioning_uri = mfa_svc.get_provisioning_uri(secret, user.email or "user")

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=BaseResponseDTO(
                    transactionUrn=getattr(request.state, "urn", "") or "",
                    status=APIStatus.SUCCESS,
                    responseMessage="Scan QR with authenticator app, then call verify to enable.",
                    responseKey="success_mfa_setup",
                    data={
                        "secret": secret,
                        "provisioningUri": provisioning_uri,
                    },
                ).model_dump(),
            )
        except Exception as err:
            return self._handle_controller_exception(request=request, err=err)


__all__ = ["MFASetupController"]
