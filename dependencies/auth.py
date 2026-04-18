"""Auth dependency helpers for routes/tests."""

from __future__ import annotations

from constants.default import Default
from constants.response_key import ResponseKey
from fast_platform.errors import UnauthorizedError
from fastapi import Request


class AuthDependency:
    """Dependency class for authentication-related operations."""

    @staticmethod
    def get_current_user(request: Request) -> dict:
        """Return authenticated user from request state or raise 401.
        
        Args:
            request: The FastAPI request object.
            
        Returns:
            The current user dictionary.
            
        Raises:
            UnauthorizedError: If user is not authenticated.
        """
        user = getattr(request.state, "user", None)
        if user is None:
            raise UnauthorizedError(
                responseMessage=Default.AUTHENTICATION_REQUIRED_MESSAGE,
                responseKey=ResponseKey.UNAUTHORIZED,
            )
        return user


__all__ = ["AuthDependency"]
