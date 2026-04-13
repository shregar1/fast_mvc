"""
POST /user/phone/verify-otp – Verify OTP and log in or complete registration.
"""



from collections.abc import Callable
from http import HTTPStatus

from typing import Optional

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from redis import Redis
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dependencies.cache import CacheDependency
from dependencies.db import DBDependency
from dependencies.repositiories.user import UserRepositoryDependency
from dependencies.utilities.dictionary import DictionaryUtilityDependency
from dependencies.utilities.jwt import JWTUtilityDependency
from dtos.requests.user.phone_verify_otp import PhoneVerifyOtpRequestDTO
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import (
    BadInputError,
    NotFoundError,
    ServiceUnavailableError,
    UnexpectedResponseError,
)
from repositories.user.refresh_token_repository import RefreshTokenRepository
from repositories.user.user_repository import UserRepository
from services.user.phone_otp import PhoneOtpService
from services.user.phone_verify_service import verify_otp_and_issue_tokens
from utilities.dictionary import DictionaryUtility
from utilities.jwt import JWTUtility


class PhoneVerifyOtpController:
    async def post(
        self,
        request: Request,
        body: PhoneVerifyOtpRequestDTO,
        session: Session = Depends(DBDependency.derive),
        redis_client: Optional[Redis] = Depends(CacheDependency.derive),
        user_repository: UserRepository = Depends(UserRepositoryDependency.derive),
        jwt_utility: JWTUtility = Depends(JWTUtilityDependency.derive),
        dictionary_utility: Callable = Depends(DictionaryUtilityDependency.derive),
    ) -> JSONResponse:
        """
        Verify OTP. Purpose must match send-otp. For purpose login/register: issue tokens (or create account for register).
        For any other purpose: return verified=true only (generic use).
        """
        urn = getattr(request.state, "urn", "") or ""
        if not redis_client:
            return JSONResponse(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                content=BaseResponseDTO(
                    transactionUrn=urn,
                    status=APIStatus.FAILED,
                    responseMessage="OTP verification is temporarily unavailable.",
                    responseKey="error_service_unavailable",
                    data={},
                ).model_dump(),
            )
        dict_util = dictionary_utility(
            urn=urn,
            user_urn=None,
            api_name="phone_verify_otp",
            user_id=None,
        )
        repo = user_repository(
            urn=urn,
            user_urn=None,
            api_name="phone_verify_otp",
            session=session,
            user_id=None,
        )
        jwt_util = jwt_utility(
            urn=urn,
            user_urn=None,
            api_name="phone_verify_otp",
            user_id=None,
        )
        try:
            otp_service = PhoneOtpService(redis_client=redis_client, urn=urn, api_name="phone_verify_otp")
            refresh_repo = RefreshTokenRepository(session) if session else None
            response_dto = await verify_otp_and_issue_tokens(
                phone=body.phone,
                otp=body.otp,
                purpose=body.purpose,
                otp_service=otp_service,
                session=session,
                user_repository=repo,
                jwt_utility=jwt_util,
                refresh_token_repository=refresh_repo,
                urn=urn,
            )
            content = dict_util.convert_dict_keys_to_camel_case(response_dto.model_dump()) if dict_util else response_dto.model_dump()
            return JSONResponse(status_code=HTTPStatus.OK, content=content)
        except (BadInputError, NotFoundError) as err:
            response_dto = BaseResponseDTO(
                transactionUrn=urn,
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
            )
            code = err.httpStatusCode if hasattr(err, "httpStatusCode") else HTTPStatus.BAD_REQUEST
            content = dict_util.convert_dict_keys_to_camel_case(response_dto.model_dump()) if dict_util else response_dto.model_dump()
            return JSONResponse(status_code=code, content=content)
        except (ServiceUnavailableError, UnexpectedResponseError) as err:
            response_dto = BaseResponseDTO(
                transactionUrn=urn,
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
            )
            content = dict_util.convert_dict_keys_to_camel_case(response_dto.model_dump()) if dict_util else response_dto.model_dump()
            return JSONResponse(status_code=err.httpStatusCode, content=content)
        except Exception as e:
            response_dto = BaseResponseDTO(
                transactionUrn=urn,
                status=APIStatus.FAILED,
                responseMessage="Verification failed.",
                responseKey="error_internal_server_error",
                data={},
            )
            content = dict_util.convert_dict_keys_to_camel_case(response_dto.model_dump()) if dict_util else response_dto.model_dump()
            return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content=content)


__all__ = ["PhoneVerifyOtpController"]
