"""Abstraction for REST API controllers."""

from __future__ import annotations

from collections.abc import Callable
from http import HTTPStatus
from typing import Any, Optional

from fastapi import Request
from fastapi.responses import JSONResponse

from controllers.abstraction import IController
from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO


class IAPIController(IController):
    """Interface for controllers under ``controllers/apis``.

    Provides :meth:`invoke_with_exception_handling` for uniform JSON error
    envelopes and :meth:`_handle_controller_exception` for inline error
    handling.
    """

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            **kwargs,
        )

    async def invoke_with_exception_handling(
        self,
        request: Request,
        handler: Callable,
    ) -> JSONResponse:
        """Run *handler* and catch any exception into a JSON error envelope."""
        try:
            return await handler()
        except Exception as err:
            urn = getattr(request.state, "urn", "") if hasattr(request, "state") else ""
            self.logger.error("Unhandled error in %s: %s", self.__class__.__name__, err)
            response_dto = BaseResponseDTO(
                transactionUrn=urn or "",
                status=APIStatus.FAILED,
                responseMessage=str(err),
                responseKey="error_internal_server_error",
                data={},
            )
            return JSONResponse(
                content=response_dto.model_dump(),
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def _handle_controller_exception(
        self,
        err: Exception,
        urn: str = "",
        http_status: int = HTTPStatus.INTERNAL_SERVER_ERROR,
    ) -> JSONResponse:
        """Build a JSON error envelope from *err*."""
        response_message = getattr(err, "responseMessage", str(err))
        response_key = getattr(err, "responseKey", "error_internal_server_error")
        status_code = getattr(err, "httpStatusCode", http_status)
        response_dto = BaseResponseDTO(
            transactionUrn=urn or "",
            status=APIStatus.FAILED,
            responseMessage=response_message,
            responseKey=response_key,
            data={},
        )
        return JSONResponse(
            content=response_dto.model_dump(),
            status_code=status_code,
        )
