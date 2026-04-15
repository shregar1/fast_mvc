"""
User Subscription Controller Module.

Handles GET /user/subscription to return the current user's active subscription.
"""

from collections.abc import Callable
from http import HTTPStatus
from typing import Any

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_lk import APILK
from constants.api_status import APIStatus
from controllers.auth.user.abstraction import IUserController
from dependencies.db import DBDependency
from dependencies.repositiories.subscription import SubscriptionRepositoryDependency
from dependencies.services.user.subscription import UserSubscriptionServiceDependency
from dependencies.utilities.dictionary import DictionaryUtilityDependency
from dtos.responses.base import BaseResponseDTO
from repositories.user.subscription_repository import SubscriptionRepository
from utilities.dictionary import DictionaryUtility

class UserSubscriptionController(IUserController):
    """
    Controller for GET /user/subscription.

    Returns the authenticated user's current active subscription, if any.
    """

    def __init__(self, urn: str | None = None, *args: Any, **kwargs: Any) -> None:
        super().__init__(urn=urn, api_name=APILK.SUBSCRIPTION, *args, **kwargs)

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
            self.bind_request_context(
                request,
                dictionary_utility_factory=dictionary_utility,
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
        except Exception as err:
            response_dto, http_status = self.handle_exception(
                err,
                request,
                event_name="subscription.fetch",
                session=session,
                force_http_ok=False,
                fallback_message="Failed to fetch subscription.",
            )

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
