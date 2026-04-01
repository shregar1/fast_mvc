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


class JWTAuthHelper:
    """Helper class for JWT authentication operations."""

    @staticmethod
    def decode_token(token: str, urn: str) -> dict:
        """Decode a JWT token and return the payload.

        Args:
            token: The JWT token to decode.
            urn: The URN for logging/context.

        Returns:
            The decoded token payload, or empty dict with user_id=None if unavailable.
        """
        if JWTUtility:
            return JWTUtility(secret_key=SECRET_KEY, algorithm=ALGORITHM, urn=urn).decode_token(token=token)
        # Fallback: return empty payload for development
        logger.warning("JWTUtility not available, returning empty payload")
        return {"user_id": None}

    @staticmethod
    def load_user(user_data: dict, urn: str):
        """Load user from database.
        
        Args:
            user_data: Dictionary containing user information (e.g., user_id).
            urn: The URN for logging/context.
            
        Returns:
            The user object if found, None otherwise.
        """
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

    @staticmethod
    def on_authenticated(request: Request, user_data: dict) -> None:
        """Callback when authentication succeeds.

        Args:
            request: The FastAPI request object.
            user_data: Dictionary containing user information.
        """
        request.state.user_id = user_data.get("user_id")

    @staticmethod
    def build_error_response(urn: str, kind: str, error) -> JSONResponse:
        """Build error response for authentication failures.

        Args:
            urn: The transaction URN.
            kind: The error kind/type.
            error: The error object or message.

        Returns:
            JSONResponse with authentication error details.
        """
        return JSONResponse(
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
        )


class NoOpAuthMiddleware:
    """No-op authentication middleware for development without fastmiddleware."""

    def __init__(self, app):
        """Initialize with ASGI app.

        Args:
            app: The ASGI application.
        """
        self.app = app

    async def __call__(self, scope, receive, send):
        """Pass through to the wrapped application.

        Args:
            scope: The ASGI connection scope.
            receive: The ASGI receive channel.
            send: The ASGI send channel.

        Returns:
            The result of the wrapped application.
        """
        await self.app(scope, receive, send)


# Create the middleware only if dependencies are available
if JWTBearerAuthMiddleware:
    AuthenticationMiddleware = partial(
        JWTBearerAuthMiddleware,
        unprotected_paths=unprotected_routes,
        callback_paths=callback_routes,
        decode_bearer=JWTAuthHelper.decode_token,
        load_user=JWTAuthHelper.load_user,
        on_authenticated=JWTAuthHelper.on_authenticated,
        build_error_response=JWTAuthHelper.build_error_response,
    )
else:
    AuthenticationMiddleware = NoOpAuthMiddleware


# Backward compatibility: module-level functions delegate to the class
_decode_token = JWTAuthHelper.decode_token
_load_user = JWTAuthHelper.load_user
_on_authenticated = JWTAuthHelper.on_authenticated


__all__ = [
    "JWTAuthHelper",
    "NoOpAuthMiddleware",
    "AuthenticationMiddleware",
]
