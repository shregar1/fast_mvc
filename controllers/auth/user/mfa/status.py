"""GET /user/mfa/status – Return whether MFA is enabled for current user."""

from http import HTTPStatus

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dependencies.db import DBDependency
from dtos.responses.base import BaseResponseDTO
from fast_database.persistence.models.user import User
from controllers.apis.v1.abstraction import IV1APIController
from constants.api_lk import APILK


class MFAStatusController(IV1APIController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name=APILK.MFA_STATUS)

    async def get(
        self,
        request: Request,
        session: Session = Depends(DBDependency.derive),
    ) -> JSONResponse:
        """
        GET /user/mfa/status – Return whether MFA is enabled for the current user.
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

            enabled = bool(getattr(user, "mfa_enabled", False))

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=BaseResponseDTO(
                    transactionUrn=getattr(request.state, "urn", "") or "",
                    status=APIStatus.SUCCESS,
                    responseMessage="Fetched MFA status.",
                    responseKey="success_mfa_status",
                    data={"enabled": enabled},
                ).model_dump(),
            )
        except Exception as err:
            return self._handle_controller_exception(request=request, err=err)


__all__ = ["MFAStatusController"]
