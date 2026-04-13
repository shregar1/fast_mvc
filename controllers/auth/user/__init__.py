"""
User Controllers Router Module.

This module serves as the entry point for all user-related endpoints.
It registers routes for user authentication operations including
login, registration, and logout.

Routes:
    POST /user/login    - User authentication
    POST /user/refresh  - Exchange refresh token for new access/refresh tokens
    POST /user/register - New user registration
    POST /user/logout   - User session termination
    GET  /user/verify-email - Verify email from link (?token=...); same as GET /user/auth/verify-email
    /user/auth/*  - Shared auth (verify-mfa, verify-email, send-verification-email)
    /user/mfa/*   - Shared MFA (setup, verify, disable, status, QR)

Usage:
    >>> from controllers.user import router
    >>> app.include_router(router)
"""



from fastapi import APIRouter
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from constants.api_lk import APILK
from controllers.user.abstraction import IUserController
from controllers.user.auth import router as user_auth_router
from controllers.user.auth.verify_email import VerifyEmailController as AuthVerifyEmailController
from controllers.user.mfa import router as user_mfa_router
from controllers.apis.v1.me import router as me_router
from controllers.user.forgot_password import forgot_password
from controllers.user.login import UserLoginController
from controllers.user.logout import UserLogoutController
from controllers.user.phone.send_otp import PhoneSendOtpController
from controllers.user.phone.verify_otp import PhoneVerifyOtpController
from controllers.user.refresh_token import UserRefreshTokenController
from controllers.user.register import UserRegistrationController
from controllers.user.subscription import UserSubscriptionController
from controllers.user.reset_password import reset_password
from start_utils import logger
from dependencies.db import DBDependency
from dtos.requests.user.forgot_password import ForgotPasswordRequestDTO
from dtos.requests.user.reset_password import ResetPasswordRequestDTO

router = APIRouter(prefix="/user")
"""User router with /user prefix. Handles authentication operations."""


class ForgotPasswordController(IUserController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name="USER_FORGOT_PASSWORD")

    async def post(
        self,
        request: Request,
        body: ForgotPasswordRequestDTO,
        session: Session = Depends(DBDependency.derive),
    ) -> JSONResponse:
        return await forgot_password(request=request, body=body, session=session)


class ResetPasswordController(IUserController):
    def __init__(self, urn: str | None = None) -> None:
        super().__init__(urn=urn, api_name="USER_RESET_PASSWORD")

    async def post(
        self,
        request: Request,
        body: ResetPasswordRequestDTO,
        session: Session = Depends(DBDependency.derive),
    ) -> JSONResponse:
        return await reset_password(request=request, body=body, session=session)


# Register login route
LOGIN_RESPONSE_EXAMPLE = {
    200: {
        "description": "Login successful",
        "content": {
            "application/json": {
                "example": {
                    "transactionUrn": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
                    "status": "SUCCESS",
                    "responseMessage": "Successfully logged in the user.",
                    "responseKey": "success_user_login",
                    "data": {
                        "status": True,
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "userUrn": "urn:user:01ARZ3NDEKTSV4RRFFQ69G5FAV",
                        "userId": 1,
                    },
                }
            }
        },
    },
}
logger.debug(f"Registering {UserLoginController.__name__} route.")
router.add_api_route(
    path="/login",
    endpoint=UserLoginController().post,
    methods=["POST"],
    name=APILK.LOGIN,
    responses=LOGIN_RESPONSE_EXAMPLE,
)
logger.debug(f"Registered {UserLoginController.__name__} route.")

# Register registration route
logger.debug(f"Registering {UserRegistrationController.__name__} route.")
router.add_api_route(
    path="/register",
    endpoint=UserRegistrationController().post,
    methods=["POST"],
    name=APILK.REGISTRATION,
)
logger.debug(f"Registered {UserRegistrationController.__name__} route.")

# Email verification (public; token from verification email)
logger.debug("Registering GET /user/verify-email.")
router.add_api_route(
    path="/verify-email",
    endpoint=AuthVerifyEmailController().get,
    methods=["GET"],
    name="USER_VERIFY_EMAIL",
)
logger.debug("Registered GET /user/verify-email.")

# Register refresh token route
logger.debug(f"Registering {UserRefreshTokenController.__name__} route.")
router.add_api_route(
    path="/refresh",
    endpoint=UserRefreshTokenController().post,
    methods=["POST"],
    name=APILK.REFRESH,
)
logger.debug(f"Registered {UserRefreshTokenController.__name__} route.")

# Register logout route
logger.debug(f"Registering {UserLogoutController.__name__} route.")
router.add_api_route(
    path="/logout",
    endpoint=UserLogoutController().post,
    methods=["POST"],
    name=APILK.LOGOUT,
)
logger.debug(f"Registered {UserLogoutController.__name__} route.")

# Register subscription route
logger.debug(f"Registering {UserSubscriptionController.__name__} route.")
router.add_api_route(
    path="/subscription",
    endpoint=UserSubscriptionController().get,
    methods=["GET"],
    name=APILK.SUBSCRIPTION,
)
logger.debug(f"Registered {UserSubscriptionController.__name__} route.")

# Phone OTP (login / register)
logger.debug("Registering user phone OTP routes.")
router.add_api_route(
    path="/phone/send-otp",
    endpoint=PhoneSendOtpController().post,
    methods=["POST"],
    name="USER_PHONE_SEND_OTP",
)
router.add_api_route(
    path="/phone/verify-otp",
    endpoint=PhoneVerifyOtpController().post,
    methods=["POST"],
    name="USER_PHONE_VERIFY_OTP",
)
logger.debug("Registered user phone OTP routes.")

# Password reset (public / unauthenticated)
logger.debug("Registering user password-reset routes.")
router.add_api_route(
    path="/forgot-password",
    endpoint=ForgotPasswordController().post,
    methods=["POST"],
    name="USER_FORGOT_PASSWORD",
)
router.add_api_route(
    path="/reset-password",
    endpoint=ResetPasswordController().post,
    methods=["POST"],
    name="USER_RESET_PASSWORD",
)
logger.debug("Registered user password-reset routes.")

# Shared auth & MFA (same paths for any app using this backend; not under /api/v1)
logger.debug("Registering shared /user/auth and /user/mfa routes.")
router.include_router(user_auth_router)
router.include_router(user_mfa_router)
router.include_router(me_router)
logger.debug("Registered shared /user/auth and /user/mfa routes.")

