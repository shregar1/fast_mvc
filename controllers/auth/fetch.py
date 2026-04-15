"""FetchUser Core Controller."""

from collections.abc import Callable

from fastapi import Depends, Request

from constants.api_status import APIStatus
from controllers.auth.abstraction import IAuthController
from dependencies.services.user.fetch import FetchUserServiceDependency
from dtos.responses.abstraction import IResponseDTO


class FetchUserController(IAuthController):
    """Represents the FetchUserController class."""

    async def handle(
        self,
        request: Request,
        urn: str,
        payload: dict,
        api_name: str,
        service_factory: Callable = Depends(FetchUserServiceDependency.derive),
    ) -> IResponseDTO:
        """Validate, delegate to FetchUserService via DI, and return a response DTO."""
        try:
            await self.validate_request(
                urn=urn, request_payload=payload, api_name=api_name,
            )
            service = service_factory(
                urn=urn,
                api_name=api_name,
            )
            result = service.run(payload)
            return IResponseDTO(
                transactionUrn=urn,
                status=APIStatus.SUCCESS,
                responseMessage=result.get("message", "User fetched successfully."),
                responseKey="success_user_fetch",
                data=result.get("item", {}),
            )
        except Exception as err:
            response_dto, _ = self.handle_exception(
                err,
                request,
                event_name="user.fetch",
                force_http_ok=False,
                fallback_message="Failed to fetch user.",
            )
            return response_dto
