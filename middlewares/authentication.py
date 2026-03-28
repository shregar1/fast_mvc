"""App-specific wiring for :class:`JWTBearerAuthMiddleware` from ``fastmiddleware``.

JWT decode and user session lookup use this application's repositories and DTOs.

Note: This middleware requires fast-mvc[platform] for full functionality.
Without the platform package, it will pass through all requests (development mode).
"""

from http import HTTPStatus
from functools import partial

from fastapi import Request
from fastapi.responses import JSONResponse

from constants.api_status import APIStatus
from constants.http_header import HttpHeader
from dtos.responses.apis import IResponseAPIDTO

# Optional dependencies (requires fast-mvc[platform])
try:
    from fast_middleware.sec.jwt_bearer_auth import JWTBearerAuthMiddleware
except ImportError:
    JWTBearerAuthMiddleware = None  # type: ignore

# JWT Utility dependency
try:
    from fast_platform.core.utils import JWTUtility
except ImportError:
    JWTUtility = None  # type: ignore

try:
    from fast_database.persistence.repositories.user import UserRepository
except ImportError:
    UserRepository = None  # type: ignore

from start_utils import (
    ALGORITHM,
    SECRET_KEY,
    callback_routes,
    db_session,
    logger,
    unprotected_routes,
)


def _decode_token(token: str, urn: str) -> dict:
    """Execute _decode_token operation.

    Args:
        token: The token parameter.
        urn: The urn parameter.

    Returns:
        The result of the operation.
    """
    if JWTUtility:
        return JWTUtility(secret_key=SECRET_KEY, algorithm=ALGORITHM, urn=urn).decode_token(token=token)
    # Fallback: return empty payload for development
    logger.warning("JWTUtility not available, returning empty payload")
    return {"user_id": None}


def _load_user(user_data: dict, urn: str):
    """Load user from database."""
    if UserRepository and db_session:
        return UserRepository(
            urn=urn, session=db_session
        ).retrieve_record_by_id_and_is_logged_in(
            id=user_data.get("user_id") or "",
            is_logged_in=True,
            is_deleted=False,
        )
    # Fallback: return None for development
    logger.warning("UserRepository not available, returning None")
    return None


def _on_authenticated(request: Request, user_data: dict) -> None:
    """Execute _on_authenticated operation.

    Args:
        request: The request parameter.
        user_data: The user_data parameter.
    """
    request.state.user_id = user_data.get("user_id")


class NoOpAuthMiddleware:
    """No-op authentication middleware for development without fastmiddleware."""

    def __init__(self, app):
        """Execute __init__ operation.

        Args:
            app: The app parameter.
        """
        self.app = app

    async def __call__(self, scope, receive, send):
        """Execute __call__ operation.

        Args:
            scope: The scope parameter.
            receive: The receive parameter.
            send: The send parameter.

        Returns:
            The result of the operation.
        """
        await self.app(scope, receive, send)


# Create the middleware only if dependencies are available
if JWTBearerAuthMiddleware:
    AuthenticationMiddleware = partial(
        JWTBearerAuthMiddleware,
        unprotected_paths=unprotected_routes,
        callback_paths=callback_routes,
        decode_bearer=_decode_token,
        load_user=_load_user,
        on_authenticated=_on_authenticated,
        build_error_response=lambda urn, kind, error: JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content=IResponseAPIDTO(
                transactionUrn=urn,
                status=APIStatus.FAILED,
                responseMessage=getattr(error, "message", str(error))
                if error
                else f"Authentication failed: {kind}",
                responseKey=f"error_{kind.lower()}",
                data={},
                errors=None,
            ).model_dump(mode="json"),
            headers=HttpHeader().get_reference_urn_header(reference_urn=urn),
        ),
    )
else:
    AuthenticationMiddleware = NoOpAuthMiddleware
