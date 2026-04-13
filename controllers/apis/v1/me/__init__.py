"""``/user/me`` – authenticated user profile endpoint."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dependencies.db import DBDependency
from dtos.responses.base import BaseResponseDTO
from fast_database.persistence.models.user import User

router = APIRouter(prefix="/me", tags=["me"])


@router.get("")
async def get_me(
    request: Request,
    session: Session = Depends(DBDependency.derive),
):
    """Return current authenticated user's profile."""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={"detail": "Authentication required"},
        )

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"detail": "User not found"},
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=BaseResponseDTO(
            transactionUrn=getattr(request.state, "urn", ""),
            status=APIStatus.SUCCESS,
            responseMessage="User profile retrieved.",
            responseKey="success_user_profile",
            data={
                "userId": user.id,
                "email": user.email,
                "userUrn": getattr(user, "urn", ""),
                "mfaEnabled": getattr(user, "mfa_enabled", False),
                "emailVerified": getattr(user, "email_verified", False),
                "phone": getattr(user, "phone", None),
                "phoneVerified": getattr(user, "phone_verified", False),
            },
        ).model_dump(),
    )


__all__ = ["router"]
