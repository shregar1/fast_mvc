"""GET /user/mfa/setup/qr-code – Return QR code image for authenticator app setup."""

import io
from http import HTTPStatus

from fastapi import Depends, Request
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dependencies.db import DBDependency
from dtos.responses.base import BaseResponseDTO
from fast_database.persistence.models.user import User
from services.mfa import MFAService
from controllers.apis.v1.abstraction import IV1APIController
from constants.api_lk import APILK

try:
    import qrcode  # type: ignore[import-not-found]
except ImportError:
    qrcode = None  # type: ignore


class MFASetupQrCodeController(IV1APIController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name=APILK.MFA_SETUP_QR_CODE)

    async def get(
        self,
        request: Request,
        session: Session = Depends(DBDependency.derive),
    ) -> Response:
        """
        GET /user/mfa/setup/qr-code – Return a PNG QR code for pending MFA setup.
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

            secret = getattr(user, "mfa_secret", None)
            if not secret:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", ""),
                        status=APIStatus.FAILED,
                        responseMessage="Call POST /mfa/setup first.",
                        responseKey="error_bad_input",
                        data={},
                    ).model_dump(),
                )

            if qrcode is None:
                return JSONResponse(
                    status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                    content=BaseResponseDTO(
                        transactionUrn=getattr(request.state, "urn", ""),
                        status=APIStatus.FAILED,
                        responseMessage=(
                            "QR code generation not available. Use data.provisioningUri from "
                            "POST /mfa/setup to generate a QR client-side."
                        ),
                        responseKey="error_service_unavailable",
                        data={"provisioningUri": MFAService().get_provisioning_uri(secret, user.email or "user")},
                    ).model_dump(),
                )

            uri = MFAService().get_provisioning_uri(secret, user.email or "user")
            img = qrcode.make(uri)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            return Response(content=buf.read(), media_type="image/png")
        except Exception as err:
            return self._handle_controller_exception(request=request, err=err)


__all__ = ["MFASetupQrCodeController"]
