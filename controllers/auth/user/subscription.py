"""
User Subscription Controller Module.

Handles GET /user/subscription to return the current user's active subscription.
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
from dependencies.repositiories.subscription import SubscriptionRepositoryDependency
from dependencies.services.user.subscription import UserSubscriptionServiceDependency
from dependencies.utilities.dictionary import DictionaryUtilityDependency
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
from repositories.user.subscription_repository import SubscriptionRepository
from utilities.dictionary import DictionaryUtility


class UserSubscriptionController(IUserController):
    """
    Controller for GET /user/subscription.

    Returns the authenticated user's current active subscription, if any.
    """



    def __init__(self, urn: str = None) -> None:
        super().__init__(urn)
        self._urn = urn
        self._user_urn = None
        self._api_name = APILK.SUBSCRIPTION
        self._user_id = None
        self._logger = self.logger
        self._dictionary_utility = None

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

    async def get(
        self,
        request: Request,
        session: Session = Depends(DBDependency.derive),
        subscription_repository_factory: Callable = Depends(
            SubscriptionRepositoryDependency.derive
        ),
        user_subscription_service_factory: Callable = Depends(
            UserSubscriptionServiceDependency.derive
        ),
        dictionary_utility: DictionaryUtility = Depends(
            DictionaryUtilityDependency.derive
        ),
    ) -> JSONResponse:
        """
        Handle GET /user/subscription.

        Returns the current user's active subscription. Requires authentication.
        """


        try:
            self.urn = request.state.urn
            self.user_id = getattr(request.state, "user_id", None)
            self.user_urn = getattr(request.state, "user_urn", None)
            self.logger = self.logger.bind(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
            )
            self.dictionary_utility = dictionary_utility(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
            )
            subscription_repository: SubscriptionRepository = (
                subscription_repository_factory(session=session)
            )
            service = user_subscription_service_factory(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                user_id=self.user_id,
                subscription_repository=subscription_repository,
            )
            response_dto: BaseResponseDTO = await service.get_current()
            http_status = HTTPStatus.OK
        except (BadInputError, ConflictError, ForbiddenError, NotFoundError, RateLimitError, ServiceUnavailableError, UnauthorizedError, UnexpectedResponseError) as err:
            urn = getattr(self, "_urn", None) or getattr(request.state, "urn", "")
            response_dto = BaseResponseDTO(
                transactionUrn=urn,
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
            )
            http_status = err.httpStatusCode
        except (UnexpectedResponseError, Exception) as err:
            self.logger.error(
                "Error fetching user subscription: %s", err, exc_info=True
            )
            urn = getattr(self, "_urn", None) or getattr(request.state, "urn", "")
            response_dto = BaseResponseDTO(
                transactionUrn=urn,
                status=APIStatus.FAILED,
                responseMessage="Failed to fetch subscription.",
                responseKey="error_internal_server_error",
                data={},
            )
            http_status = HTTPStatus.INTERNAL_SERVER_ERROR

        util = self.dictionary_utility
        if util is None:
            try:
                util = dictionary_utility(
                    urn=getattr(self, "_urn", ""),
                    user_urn=getattr(self, "_user_urn", ""),
                    api_name=self._api_name,
                    user_id=getattr(self, "_user_id", None),
                )
            except Exception:
                util = None

        content = (
            util.convert_dict_keys_to_camel_case(response_dto.model_dump())
            if util is not None
            else response_dto.model_dump()
        )
        return JSONResponse(content=content, status_code=http_status)
