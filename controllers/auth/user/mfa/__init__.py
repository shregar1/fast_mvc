from fastapi import APIRouter

from constants.api_lk import APILK
from controllers.auth.user.mfa.disable import MFADisableController
from controllers.auth.user.mfa.qr_code import MFASetupQrCodeController
from controllers.auth.user.mfa.setup import MFASetupController
from controllers.auth.user.mfa.status import MFAStatusController
from controllers.auth.user.mfa.verify import MFAVerifyController

__all__ = [
    "MFASetupController",
    "MFASetupQrCodeController",
    "MFAVerifyController",
    "MFADisableController",
    "MFAStatusController",
]

router = APIRouter(prefix="/mfa")

router.add_api_route(
    path="/setup",
    endpoint=MFASetupController().post,
    methods=["POST"],
    name=APILK.MFA_SETUP,
)
router.add_api_route(
    path="/setup/qr-code",
    endpoint=MFASetupQrCodeController().get,
    methods=["GET"],
    name=APILK.MFA_SETUP_QR_CODE,
)
router.add_api_route(
    path="/verify",
    endpoint=MFAVerifyController().post,
    methods=["POST"],
    name=APILK.MFA_VERIFY,
)
router.add_api_route(
    path="/disable",
    endpoint=MFADisableController().post,
    methods=["POST"],
    name=APILK.MFA_DISABLE,
)
router.add_api_route(
    path="/status",
    endpoint=MFAStatusController().get,
    methods=["GET"],
    name=APILK.MFA_STATUS,
)

__all__ = [*__all__, "router"]
