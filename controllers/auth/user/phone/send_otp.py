"""
POST /user/phone/send-otp – Send OTP to phone for login or register.
"""



from http import HTTPStatus

from typing import Optional

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from redis import Redis
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dependencies.cache import CacheDependency
from dependencies.db import DBDependency
from dtos.requests.user.phone_send_otp import PhoneSendOtpRequestDTO
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import BadInputError, UnexpectedResponseError
from services.user.phone_otp import PhoneOtpService
from start_utils import logger


class PhoneSendOtpController:
    async def post(
        self,
        request: Request,
        body: PhoneSendOtpRequestDTO,
        session: Session = Depends(DBDependency.derive),
        redis_client: Optional[Redis] = Depends(CacheDependency.derive),
    ) -> JSONResponse:
        """
        Send a 6-digit OTP to the given phone for any purpose (e.g. login, register, verify_phone, reset_password).
        OTP is valid for 5 minutes. Same purpose must be used when verifying. Always return same message to avoid enumeration.
        """
        urn = getattr(request.state, "urn", "") or ""
        try:
            if not redis_client:
                raise UnexpectedResponseError(
                    responseMessage="OTP service is temporarily unavailable.",
                    responseKey="error_service_unavailable",
                    httpStatusCode=HTTPStatus.SERVICE_UNAVAILABLE,
                )
            ok = PhoneOtpService(urn=urn).create_and_send_otp(
                body.phone,
                body.purpose,
                redis_client,
            )
            if not ok:
                logger.warning("Send OTP failed for phone %s", body.phone[:6] + "***")
        except (BadInputError, UnexpectedResponseError):
            raise
        except Exception as e:
            logger.warning("Send OTP error: %s", e)

        response_dto = BaseResponseDTO(
            transactionUrn=urn,
            status=APIStatus.SUCCESS,
            responseMessage="If this number is valid, you will receive an OTP shortly.",
            responseKey="success_otp_sent",
            data={},
        )
        return JSONResponse(status_code=HTTPStatus.OK, content=response_dto.model_dump())


__all__ = ["PhoneSendOtpController"]
