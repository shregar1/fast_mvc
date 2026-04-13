"""JSON API Controller base with structured error handling."""

from __future__ import annotations

from collections.abc import Callable
from http import HTTPStatus
from typing import Any

from fastapi.responses import JSONResponse

from abstractions.controller import IController
from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from start_utils import logger


class JSONAPIController(IController):
    """Base controller that wraps handler execution in a JSON error envelope.

    Sub-classes override ``post`` / ``get`` etc. and can call
    :meth:`invoke_with_exception_handling` to get uniform error wrapping.
    """

    def __init__(
        self,
        urn: str | None = None,
        user_urn: str | None = None,
        api_name: str | None = None,
        user_id: int | None = None,
    ) -> None:
        super().__init__(urn=urn, user_urn=user_urn, api_name=api_name, user_id=user_id)
        self._logger = logger

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value) -> None:
        self._logger = value

    async def invoke_with_exception_handling(
        self,
        request: Any,
        handler: Callable,
    ) -> JSONResponse:
        """Run *handler* and catch any exception into a JSON error envelope."""
        try:
            return await handler()
        except Exception as err:
            urn = getattr(request.state, "urn", "") if hasattr(request, "state") else ""
            self._logger.error("Unhandled error in %s: %s", self.__class__.__name__, err)
            response_dto = BaseResponseDTO(
                transactionUrn=urn,
                status=APIStatus.FAILED,
                responseMessage=str(err),
                responseKey="error_internal_server_error",
                data={},
            )
            return JSONResponse(
                content=response_dto.model_dump(),
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )


__all__ = ["JSONAPIController"]
