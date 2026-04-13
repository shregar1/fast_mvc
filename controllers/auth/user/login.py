"""
User Login Controller Module.

This module handles user authentication via login credentials.
It validates user input, authenticates against the database,
and returns a JWT token on successful authentication.

Endpoint:
    POST /user/login

Request Body:
    {
        "email": "user@example.com",
        "password": "SecureP@ss123"
    }

Response (success, no MFA):
    {
        "transactionUrn": "urn:request:abc123",
        "status": "SUCCESS",
        "responseMessage": "Successfully logged in the user.",
        "responseKey": "success_user_login",
        "data": {
            "status": true,
            "token": "eyJhbG...",
            "refreshToken": "eyJhbG...",
            "userUrn": "urn:user:...",
            "userId": 1,
            "publicKeyPem": "-----BEGIN PUBLIC KEY-----\\n..."
        }
    }

Response (MFA required):
    data.requiresMFA true, data.mfaChallengeToken, data.userUrn, data.publicKeyPem; no token/refreshToken.
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
from dependencies.services.user.login import UserLoginServiceDependency
from dependencies.utilities.dictionary import DictionaryUtilityDependency
from dependencies.utilities.jwt import JWTUtilityDependency
from dtos.requests.user.login import UserLoginRequestDTO
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
from structured_log import log_event
from utilities.audit import log_audit
from utilities.dictionary import DictionaryUtility
from utilities.jwt import JWTUtility
from utilities.request_utils import get_client_ip


class UserLoginController(IUserController):
    """
    Controller for user login/authentication.

    Handles POST requests to /user/login endpoint. Validates credentials,
    authenticates the user, and returns a JWT token for subsequent requests.

    Attributes:
        urn (str): Unique Request Number for this request.
        user_urn (str): User's unique resource name (set after auth).
        api_name (str): Always set to APILK.LOGIN.
        user_id (int): User's database ID (set after auth).
        dictionary_utility (DictionaryUtility): For response formatting.
        jwt_utility (JWTUtility): For token generation.

    Example:
        >>> controller = UserLoginController()
        >>> response = await controller.post(request, credentials)
    """



    def __init__(self, urn: str = None) -> None:
        """
        Initialize the login controller.

        Args:
            urn (str, optional): Unique Request Number. Defaults to None.
        """


        super().__init__(urn)
        self._urn = urn
        self._user_urn = None
        self._api_name = APILK.LOGIN
        self._user_id = None
        self._logger = self.logger
        self._dictionary_utility = None
        self._jwt_utility = None

    @property
    def urn(self) -> str:
        """str: Get the Unique Request Number."""

        return self._urn

    @urn.setter
    def urn(self, value: str) -> None:
        """Set the Unique Request Number."""

        self._urn = value

    @property
    def user_urn(self) -> str:
        """str: Get the user's unique resource name."""

        return self._user_urn

    @user_urn.setter
    def user_urn(self, value: str) -> None:
        """Set the user's unique resource name."""

        self._user_urn = value

    @property
    def api_name(self) -> str:
        """str: Get the API endpoint name."""

        return self._api_name

    @api_name.setter
    def api_name(self, value: str) -> None:
        """Set the API endpoint name."""

        self._api_name = value

    @property
    def user_id(self) -> int:
        """int: Get the user's database identifier."""

        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        """Set the user's database identifier."""

        self._user_id = value

    @property
    def logger(self):
        """loguru.Logger: Get the structured logger instance."""

        return self._logger

    @logger.setter
    def logger(self, value) -> None:
        """Set the structured logger instance."""

        self._logger = value

    @property
    def dictionary_utility(self) -> DictionaryUtility:
        """DictionaryUtility: Get the dictionary utility for response formatting."""

        return self._dictionary_utility

    @dictionary_utility.setter
    def dictionary_utility(self, value: DictionaryUtility) -> None:
        """Set the dictionary utility."""

        self._dictionary_utility = value

    @property
    def jwt_utility(self) -> JWTUtility:
        """JWTUtility: Get the JWT utility for token operations."""

        return self._jwt_utility

    @jwt_utility.setter
    def jwt_utility(self, value: JWTUtility) -> None:
        """Set the JWT utility."""

        self._jwt_utility = value

    async def post(
        self,
        request: Request,
        request_payload: UserLoginRequestDTO,
        session: Session = Depends(DBDependency.derive),
        user_repository: UserRepository = Depends(
            UserRepositoryDependency.derive
        ),
        user_login_service_factory: Callable = Depends(
            UserLoginServiceDependency.derive
        ),
        dictionary_utility: DictionaryUtility = Depends(
            DictionaryUtilityDependency.derive
        ),
        jwt_utility: JWTUtility = Depends(
            JWTUtilityDependency.derive
        )
    ) -> JSONResponse:
        """
        Handle POST request for user login.

        Authenticates user credentials and returns a JWT token on success.
        All errors are caught and returned as structured error responses.

        Args:
            request (Request): FastAPI request object with state.urn.
            request_payload (UserLoginRequestDTO): Login credentials.
            session (Session): Database session from dependency injection.
            user_repository (UserRepository): User data access dependency.
            user_login_service_factory (Callable): Factory for login service.
            dictionary_utility (DictionaryUtility): Response formatting utility.
            jwt_utility (JWTUtility): JWT token utility.

        Returns:
            JSONResponse: Contains:
                - transactionUrn: Request tracking ID
                - status: SUCCESS or FAILED
                - responseMessage: Human-readable message
                - responseKey: Machine-readable key for i18n
                - data: Token and user info on success

        Raises:
            No exceptions are raised; all errors return JSONResponse with
            appropriate HTTP status codes.

        HTTP Status Codes:
            - 200 OK: Login successful
            - 400 Bad Request: Invalid input
            - 404 Not Found: User not found
            - 500 Internal Server Error: Unexpected error
        """


        # Ensure we always have a safe fallback response even if setup fails early.
        response_dto = BaseResponseDTO(
            transactionUrn=getattr(request.state, "urn", "") or "",
            status=APIStatus.FAILED,
            responseMessage="Failed to login users.",
            responseKey="error_internal_server_error",
            data={},
        )
        httpStatusCode = HTTPStatus.OK

        def _txn_urn() -> str:
            """Best-effort URN for envelopes when setup failed before self.urn is set."""

            return (
                getattr(request.state, "urn", None)
                or self.urn
                or ""
            )

        try:
            self.logger.debug("Fetching request URN")
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
            self.jwt_utility: JWTUtility = jwt_utility(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
            )
            self.user_repository: UserRepository = user_repository(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
                session=session,
            )
            refresh_token_repo = RefreshTokenRepository(session=session)

            self.logger.debug("Validating request")
            await self.validate_request(
                urn=self.urn,
                user_urn=self.user_urn,
                request_payload=request_payload.model_dump(),
                request_headers=dict(request.headers.mutablecopy()),
                api_name=self.api_name,
                user_id=self.user_id,
            )
            self.logger.debug("Verified request")

            self.logger.debug("Running login user service")
            response_dto: BaseResponseDTO = await user_login_service_factory(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
                jwt_utility=self.jwt_utility,
                user_repository=self.user_repository,
                refresh_token_repository=refresh_token_repo,
            ).run(request_dto=request_payload)

            self.logger.debug("Preparing response metadata")
            httpStatusCode = HTTPStatus.OK
            if response_dto.status == APIStatus.SUCCESS and getattr(response_dto, "data", None):
                try:
                    uid = response_dto.data.get("user_id")
                    log_audit(
                        session,
                        "login.success",
                        "user",
                        actor_id=uid,
                        actor_urn=response_dto.data.get("user_urn"),
                        resource_id=str(uid),
                        ip=get_client_ip(request),
                    )
                    log_event(
                        "login.success",
                        user_id=uid,
                        urn=self.urn,
                        user_urn=response_dto.data.get("user_urn"),
                    )
                except Exception:
                    pass
            self.logger.debug("Prepared response metadata")

        except (BadInputError, ConflictError, ForbiddenError, NotFoundError, UnauthorizedError) as err:
            self.logger.error(
                f"{err.__class__} error occurred while logging in user: {err}"
            )
            response_dto = BaseResponseDTO(
                transactionUrn=_txn_urn(),
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
            )
            # Contract tests expect auth endpoints to always return 200,
            # even when the response body indicates FAILED.
            httpStatusCode = HTTPStatus.OK
            log_event(
                "login.failed",
                level="warning",
                urn=_txn_urn(),
                reason=err.responseKey,
                status_code=err.httpStatusCode,
            )
            try:
                log_audit(
                    session,
                    "login.failed",
                    "user",
                    resource_id=None,
                    metadata={"reason": err.responseKey},
                    ip=get_client_ip(request),
                )
            except Exception:
                pass

        except (RateLimitError, ServiceUnavailableError, UnexpectedResponseError) as err:
            self.logger.error(
                f"{err.__class__} error occurred while logging in user: {err}"
            )
            log_event(
                "login.failed",
                level="warning",
                urn=_txn_urn(),
                reason=err.responseKey,
                status_code=err.httpStatusCode,
            )
            response_dto = BaseResponseDTO(
                transactionUrn=_txn_urn(),
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
            )
            httpStatusCode = HTTPStatus.OK

        except Exception as err:
            self.logger.error(
                f"{err.__class__} error occurred while logging in user: {err}"
            )
            log_event(
                "login.failed",
                level="error",
                urn=_txn_urn(),
                reason="internal_error",
            )
            response_dto = BaseResponseDTO(
                transactionUrn=_txn_urn(),
                status=APIStatus.FAILED,
                responseMessage="Failed to login users.",
                responseKey="error_internal_server_error",
                data={},
            )
            httpStatusCode = HTTPStatus.OK
            try:
                log_audit(
                    session,
                    "login.failed",
                    "user",
                    metadata={"reason": "internal_error"},
                    ip=get_client_ip(request),
                )
            except Exception:
                pass

        dict_util = self.dictionary_utility
        content = (
            dict_util.convert_dict_keys_to_camel_case(response_dto.model_dump())
            if dict_util is not None
            else response_dto.model_dump()
        )

        return JSONResponse(
            content=content,
            status_code=httpStatusCode,
        )
