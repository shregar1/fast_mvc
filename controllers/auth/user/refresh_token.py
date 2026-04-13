"""
User Refresh Token Controller Module.

Handles exchange of a refresh token for new access and refresh tokens.
No authentication required; client sends refresh token in request body.

Endpoint:
    POST /user/refresh

Request Body:
    {
        "reference_number": "550e8400-e29b-41d4-a716-446655440000",
        "refreshToken": "eyJhbG..."
    }

Response:
    {
        "transactionUrn": "urn:request:abc123",
        "status": "SUCCESS",
        "responseMessage": "Tokens refreshed successfully.",
        "responseKey": "success_refresh_token",
        "data": {
            "token": "eyJhbG...",
            "refreshToken": "eyJhbG...",
            "user_urn": "urn:user:..."
        }
    }
"""



from collections.abc import Callable
from http import HTTPStatus

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_lk import APILK
from constants.api_status import APIStatus
from controllers.user.abstraction import IUserController
from dependencies.db import DBDependency
from dependencies.repositiories.user import UserRepositoryDependency
from dependencies.services.user.refresh_token import UserRefreshTokenServiceDependency
from dependencies.utilities.dictionary import DictionaryUtilityDependency
from dependencies.utilities.jwt import JWTUtilityDependency
from dtos.requests.user.refresh import RefreshTokenRequestDTO
from dtos.responses.base import BaseResponseDTO
from fast_platform.errors import (
    BadInputError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
    UnauthorizedError,
    UnexpectedResponseError,
)
from repositories.user.refresh_token_repository import RefreshTokenRepository
from repositories.user.user_repository import UserRepository
from utilities.audit import log_audit
from utilities.dictionary import DictionaryUtility
from utilities.jwt import JWTUtility
from utilities.request_utils import get_client_ip


class UserRefreshTokenController(IUserController):
    """
    Controller for refresh token exchange.

    Handles POST /user/refresh. Validates refresh token and returns
    new access and refresh tokens. Unauthenticated route.
    """



    def __init__(self, urn: str = None) -> None:
        super().__init__(urn)
        self._urn = urn
        self._user_urn = None
        self._api_name = APILK.REFRESH
        self._user_id = None
        self._logger = self.logger
        self._dictionary_utility = None
        self._jwt_utility = None

    @property
    def urn(self) -> str:

        return self._urn

    @urn.setter
    def urn(self, value: str) -> None:
        self._urn = value

    @property
    def user_urn(self) -> str:

        return self._user_urn

    @user_urn.setter
    def user_urn(self, value: str) -> None:
        self._user_urn = value

    @property
    def api_name(self) -> str:

        return self._api_name

    @api_name.setter
    def api_name(self, value: str) -> None:
        self._api_name = value

    @property
    def user_id(self) -> int:

        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        self._user_id = value

    @property
    def logger(self):

        return self._logger

    @logger.setter
    def logger(self, value) -> None:
        self._logger = value

    @property
    def dictionary_utility(self) -> DictionaryUtility:

        return self._dictionary_utility

    @dictionary_utility.setter
    def dictionary_utility(self, value: DictionaryUtility) -> None:
        self._dictionary_utility = value

    @property
    def jwt_utility(self) -> JWTUtility:

        return self._jwt_utility

    @jwt_utility.setter
    def jwt_utility(self, value: JWTUtility) -> None:
        self._jwt_utility = value

    async def post(
        self,
        request: Request,
        request_payload: RefreshTokenRequestDTO,
        session: Session = Depends(DBDependency.derive),
        user_repository: UserRepository = Depends(UserRepositoryDependency.derive),
        refresh_service_factory: Callable = Depends(
            UserRefreshTokenServiceDependency.derive
        ),
        dictionary_utility: DictionaryUtility = Depends(
            DictionaryUtilityDependency.derive
        ),
        jwt_utility: JWTUtility = Depends(JWTUtilityDependency.derive),
    ) -> JSONResponse:
        """Handle POST /user/refresh: exchange refresh token for new tokens."""

        try:
            self.urn = request.state.urn
            self.user_id = getattr(request.state, "user_id", None)
            self.user_urn = getattr(request.state, "user_urn", None)
            self.logger = self.logger.bind(
                urn=self.urn, user_urn=self.user_urn, api_name=self.api_name
            )
            self.dictionary_utility = dictionary_utility(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
            )
            self.jwt_utility = jwt_utility(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
            )
            self.user_repository = user_repository(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
                session=session,
            )
            refresh_token_repo = RefreshTokenRepository(session=session)

            await self.validate_request(
                urn=self.urn,
                user_urn=self.user_urn,
                request_payload=request_payload.model_dump(),
                request_headers=dict(request.headers.mutablecopy()),
                api_name=self.api_name,
                user_id=self.user_id,
            )

            response_dto: BaseResponseDTO = await refresh_service_factory(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
                jwt_utility=self.jwt_utility,
                user_repository=self.user_repository,
                refresh_token_repository=refresh_token_repo,
            ).run(request_dto=request_payload)

            http_status = HTTPStatus.OK
            if response_dto.status == APIStatus.SUCCESS and getattr(response_dto, "data", None):
                try:
                    uid = response_dto.data.get("user_id")
                    log_audit(
                        session,
                        "token.refresh",
                        "user",
                        actor_id=uid,
                        actor_urn=response_dto.data.get("user_urn"),
                        resource_id=str(uid) if uid else None,
                        ip=get_client_ip(request),
                    )
                except Exception:
                    pass

        except (BadInputError, ConflictError, ForbiddenError, NotFoundError, UnauthorizedError) as err:
            self.logger.error(
                f"{err.__class__} error while refreshing token: {err}"
            )
            response_dto = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
            )
            http_status = err.httpStatusCode
            try:
                log_audit(
                    session,
                    "token.refresh_failed",
                    "user",
                    metadata={"reason": err.responseKey},
                    ip=get_client_ip(request),
                )
            except Exception:
                pass

        except (RateLimitError, ServiceUnavailableError, UnexpectedResponseError) as err:
            self.logger.error(
                f"{err.__class__} error while refreshing token: {err}"
            )
            response_dto = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
            )
            http_status = err.httpStatusCode

        except Exception as err:
            self.logger.error(
                f"{err.__class__} error while refreshing token: {err}"
            )
            response_dto = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage="Failed to refresh tokens.",
                responseKey="error_internal_server_error",
                data={},
            )
            http_status = HTTPStatus.INTERNAL_SERVER_ERROR
            try:
                log_audit(
                    session,
                    "token.refresh_failed",
                    "user",
                    metadata={"reason": "internal_error"},
                    ip=get_client_ip(request),
                )
            except Exception:
                pass

        content = (
            self.dictionary_utility.convert_dict_keys_to_camel_case(response_dto.model_dump())
            if self.dictionary_utility is not None
            else response_dto.model_dump()
        )
        return JSONResponse(content=content, status_code=http_status)
