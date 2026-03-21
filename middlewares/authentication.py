"""
App-specific wiring for :class:`JWTBearerAuthMiddleware` from ``fastmvc_middleware``.

JWT decode and user session lookup use this application's repositories and DTOs.
"""

from http import HTTPStatus

from fastapi.responses import JSONResponse

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from fastmvc_middleware import ErrorKind, JWTBearerAuthMiddleware
from fastmvc_db_models.models.user import UserRepository
from start_utils import callback_routes, db_session, logger, unprotected_routes
from fastmvc_utilities.jwt import JWTUtility


def _decode_bearer(token: str, urn: str) -> dict:
    return JWTUtility(urn=urn).decode_token(token=token)


def _load_user(user_data: dict, urn: str):
    return UserRepository(urn=urn, session=db_session).retrieve_record_by_id_and_is_logged_in(
        id=user_data.get("user_id"),
        is_logged_in=True,
        is_deleted=False,
    )


def _on_authenticated(request, user_data: dict) -> None:
    request.state.user_id = user_data.get("user_id")
    request.state.user_urn = user_data.get("user_urn")


def _build_error(urn: str, kind: ErrorKind, _exc: BaseException | None) -> JSONResponse:
    if kind == "missing_bearer":
        dto = BaseResponseDTO(
            transactionUrn=urn,
            status=APIStatus.FAILED,
            responseMessage="JWT Authentication failed.",
            responseKey="error_authetication_error",
            data={},
        )
        return JSONResponse(content=dto.model_dump(), status_code=HTTPStatus.UNAUTHORIZED)

    if kind == "session_expired":
        dto = BaseResponseDTO(
            transactionUrn=urn,
            status=APIStatus.FAILED,
            responseMessage="User Session Expired.",
            responseKey="error_session_expiry",
        )
        return JSONResponse(content=dto.model_dump(), status_code=HTTPStatus.UNAUTHORIZED)

    if kind == "service_unavailable":
        dto = BaseResponseDTO(
            transactionUrn=urn,
            status=APIStatus.FAILED,
            responseMessage="Authentication service temporarily unavailable.",
            responseKey="error_authentication_service_unavailable",
            data={},
        )
        return JSONResponse(
            content=dto.model_dump(),
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        )

    # auth_failed, generic
    dto = BaseResponseDTO(
        transactionUrn=urn,
        status=APIStatus.FAILED,
        responseMessage="JWT Authentication failed.",
        responseKey="error_authetication_error",
        data={},
    )
    return JSONResponse(content=dto.model_dump(), status_code=HTTPStatus.UNAUTHORIZED)


class AuthenticationMiddleware(JWTBearerAuthMiddleware):
    """JWT auth for this app; see ``fastmvc_middleware.jwt_bearer_auth`` for the generic base."""

    def __init__(self, app) -> None:
        super().__init__(
            app,
            unprotected_paths=unprotected_routes,
            callback_paths=callback_routes,
            decode_bearer=_decode_bearer,
            load_user=_load_user,
            on_authenticated=_on_authenticated,
            build_error_response=_build_error,
            log=logger,
        )
