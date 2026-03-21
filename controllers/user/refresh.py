"""
User Refresh Token Controller.

POST /user/refresh – exchange a valid refresh token for new access and refresh tokens.
"""

from collections.abc import Callable
from http import HTTPStatus

from fastapi import Depends, Request
from fastapi.responses import JSONResponse

from constants.api_lk import APILK
from constants.api_status import APIStatus
from controllers.user.abstraction import IUserController
from dependencies.services.user.refresh import UserRefreshServiceDependency
from dependencies.fastmvc_utilities.dictionary import DictionaryUtilityDependency
from dependencies.utilities.jwt import JWTUtilityDependency
from dtos.requests.user.refresh import UserRefreshRequestDTO
from dtos.responses.base import BaseResponseDTO
from fastmvc_errors.bad_input_error import BadInputError
from fastmvc_utilities.dictionary import DictionaryUtility
from fastmvc_utilities.jwt import JWTUtility


class UserRefreshController(IUserController):
    """Controller for POST /user/refresh – issue new tokens from a refresh token."""

    def __init__(self, urn: str = None) -> None:
        super().__init__(urn)
        self._urn = urn
        self._api_name = APILK.REFRESH

    @property
    def api_name(self) -> str:
        return self._api_name

    async def post(
        self,
        request: Request,
        request_payload: UserRefreshRequestDTO,
        refresh_service_factory: Callable = Depends(UserRefreshServiceDependency.derive),
        dictionary_utility: DictionaryUtility = Depends(DictionaryUtilityDependency.derive),
        jwt_utility: JWTUtility = Depends(JWTUtilityDependency.derive),
    ) -> JSONResponse:
        self.urn = request.state.urn
        self.logger = self.logger.bind(urn=self.urn, api_name=self.api_name)
        dict_util = dictionary_utility(
            urn=self.urn,
            user_urn=None,
            api_name=self.api_name,
            user_id=None,
        )
        try:
            jwt_util = jwt_utility(
                urn=self.urn,
                user_urn=None,
                api_name=self.api_name,
                user_id=None,
            )
            service = refresh_service_factory(
                urn=self.urn,
                user_urn=None,
                api_name=self.api_name,
                user_id=None,
                jwt_utility=jwt_util,
            )
            response_dto: BaseResponseDTO = await service.run(
                refresh_token=request_payload.refresh_token
            )
            http_status = HTTPStatus.OK
        except BadInputError as err:
            self.logger.error("Refresh failed: %s", err)
            response_dto = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
            )
            http_status = err.httpStatusCode
        except Exception as err:
            self.logger.error("Refresh error: %s", err)
            response_dto = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage="Failed to refresh tokens.",
                responseKey="error_internal_server_error",
                data={},
            )
            http_status = HTTPStatus.INTERNAL_SERVER_ERROR

        return JSONResponse(
            content=dict_util.convert_dict_keys_to_camel_case(response_dto.model_dump()),
            status_code=http_status,
        )
