"""User-domain request DTOs."""

from . import forgot_password
from . import reset_password
from dtos.requests.user.abstraction import IRequestUserDTO
from dtos.requests.user.login import UserLoginRequestDTO
from dtos.requests.user.registration import UserRegistrationRequestDTO
from dtos.requests.user.logout import UserLogoutRequestDTO
from dtos.requests.user.refresh import RefreshTokenRequestDTO
from dtos.requests.user.forgot_password import ForgotPasswordRequestDTO
from dtos.requests.user.reset_password import ResetPasswordRequestDTO
from dtos.requests.user.phone_send_otp import PhoneSendOtpRequestDTO
from dtos.requests.user.phone_verify_otp import PhoneVerifyOtpRequestDTO

__all__ = [
    "forgot_password",
    "reset_password",
    "IRequestUserDTO",
    "UserLoginRequestDTO",
    "UserRegistrationRequestDTO",
    "UserLogoutRequestDTO",
    "RefreshTokenRequestDTO",
    "ForgotPasswordRequestDTO",
    "ResetPasswordRequestDTO",
    "PhoneSendOtpRequestDTO",
    "PhoneVerifyOtpRequestDTO",
]
