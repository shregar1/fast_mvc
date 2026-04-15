from fastapi import APIRouter

from constants.api_lk import APILK
from controllers.auth.user.account.send_verification_email import SendVerificationEmailController
from controllers.auth.user.account.verify_email import VerifyEmailController
from controllers.auth.user.account.verify_mfa import VerifyMFAController

router = APIRouter(prefix="/auth")

router.add_api_route(
    path="/verify-mfa",
    endpoint=VerifyMFAController().post,
    methods=["POST"],
    name=APILK.AUTH_VERIFY_MFA,
)
router.add_api_route(
    path="/verify-email",
    endpoint=VerifyEmailController().get,
    methods=["GET"],
    name=APILK.AUTH_VERIFY_EMAIL,
)
router.add_api_route(
    path="/send-verification-email",
    endpoint=SendVerificationEmailController().post,
    methods=["POST"],
    name=APILK.AUTH_SEND_VERIFICATION_EMAIL,
)

__all__ = ["router"]

