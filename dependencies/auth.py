"""Auth dependency helpers for routes/tests."""

from __future__ import annotations

from fastapi import HTTPException, Request, status


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
            HTTPException: 401 if user is not authenticated.
        """
        user = getattr(request.state, "user", None)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        return user


__all__ = ["AuthDependency"]
