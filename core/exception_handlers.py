"""FastAPI exception handlers for ``fast_platform.errors`` and uncaught exceptions."""

from __future__ import annotations

from functools import partial
from http import HTTPStatus
from types import ModuleType

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from constants.api_status import APIStatus
from constants.http_header import HttpHeader
from constants.log_level import LogLevelName
from constants.response_key import ResponseKey
from dtos.responses.apis.abstraction import IResponseAPIDTO


async def _platform_error_handler(
    request: Request,
    exc: BaseException,
    *,
    log_level: str,
) -> JSONResponse:
    return ApplicationExceptionHandlers.app_error_response(
        request, exc, log_level=log_level
    )


class ApplicationExceptionHandlers:
    """Install domain-error and catch-all handlers on a FastAPI application."""

    @staticmethod
    def app_error_response(
        request: Request, exc: BaseException, log_level: str = LogLevelName.WARNING
    ) -> JSONResponse:
        """Build a JSONResponse for application error types (Unauthorized, Forbidden, etc.)."""
        urn = getattr(request.state, "urn", None) or ""
        try:
            getattr(logger, log_level)(
                f"{exc.__class__.__name__}: {getattr(exc, 'responseMessage', str(exc))} (key={getattr(exc, 'responseKey', 'unknown')})",
                urn=urn,
            )
        except Exception:
            pass

        response_dto = IResponseAPIDTO(
            transactionUrn=urn,
            status=APIStatus.FAILED,
            responseMessage=getattr(exc, "responseMessage", str(exc)),
            responseKey=getattr(exc, "responseKey", "error_unknown"),
            data={},
            errors=None,
        )
        return JSONResponse(
            status_code=getattr(exc, "httpStatusCode", HTTPStatus.INTERNAL_SERVER_ERROR),
            content=response_dto.model_dump(mode="json"),
            headers=HttpHeader().get_reference_urn_header(
                reference_urn=request.headers.get(HttpHeader.X_REFERENCE_URN)
            ),
        )

    @classmethod
    def register_platform_handlers(cls, app: FastAPI, platform_errors: ModuleType) -> None:
        """Register handlers for :mod:`fast_platform.errors` exception types."""
        specs: list[tuple[type[BaseException], str]] = [
            (platform_errors.UnexpectedResponseError, LogLevelName.ERROR),
            (platform_errors.BadInputError, LogLevelName.WARNING),
            (platform_errors.NotFoundError, LogLevelName.INFO),
            (platform_errors.UnauthorizedError, LogLevelName.WARNING),
            (platform_errors.ForbiddenError, LogLevelName.WARNING),
            (platform_errors.ConflictError, LogLevelName.WARNING),
            (platform_errors.RateLimitError, LogLevelName.INFO),
            (platform_errors.ServiceUnavailableError, LogLevelName.ERROR),
        ]
        for exc_type, level in specs:
            app.add_exception_handler(
                exc_type,
                partial(_platform_error_handler, log_level=level),
            )

    @staticmethod
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch-all handler for unhandled exceptions to avoid leaking internals."""
        urn = getattr(request.state, "urn", None) or ""
        logger.exception(
            "Unhandled exception occurred while processing request.", urn=urn
        )
        response_dto = IResponseAPIDTO(
            transactionUrn=urn,
            status=APIStatus.FAILED,
            responseMessage="Internal server error.",
            responseKey=ResponseKey.ERROR_INTERNAL_SERVER_ERROR,
            data={},
            errors=None,
        )
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=response_dto.model_dump(mode="json"),
            headers=HttpHeader().get_reference_urn_header(
                reference_urn=request.headers.get(HttpHeader.X_REFERENCE_URN)
            ),
        )

    @classmethod
    def register_global_handler(cls, app: FastAPI) -> None:
        app.add_exception_handler(Exception, cls.global_exception_handler)


__all__ = ["ApplicationExceptionHandlers"]
