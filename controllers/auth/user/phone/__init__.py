"""Phone OTP login and registration – send OTP, verify OTP and issue tokens."""



from controllers.auth.user.phone.send_otp import PhoneSendOtpController
from controllers.auth.user.phone.verify_otp import PhoneVerifyOtpController

__all__ = ["PhoneSendOtpController", "PhoneVerifyOtpController"]
