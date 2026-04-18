"""``/user/me`` – authenticated user profile endpoint."""

from collections.abc import Callable
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_status import APIStatus
from dependencies.db import DBDependency
from dependencies.repositiories.user import UserRepositoryDependency
from dtos.responses.base import BaseResponseDTO

router = APIRouter(prefix="/me", tags=["me"])


@router.get("")
async def get_me(
    request: Request,
    session: Session = Depends(DBDependency.derive),
    user_repository_factory: Callable = Depends(UserRepositoryDependency.derive),
):
    """Return current authenticated user's profile."""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={"detail": "Authentication required"},
        )

    repo = user_repository_factory(
        urn=getattr(request.state, "urn", None),
        user_urn=getattr(request.state, "user_urn", None),
        api_name="USER_ME",
        user_id=user_id,
        session=session,
    )
    user = repo.retrieve_record_by_id(user_id)
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
                "mfaEnabled": user.mfa_enabled,
                "emailVerified": getattr(user, "email_verified", False),
                "phone": getattr(user, "phone", None),
                "phoneVerified": getattr(user, "phone_verified", False),
            },
        ).model_dump(),
    )


__all__ = ["router"]
