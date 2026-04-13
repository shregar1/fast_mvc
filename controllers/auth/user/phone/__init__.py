"""Phone OTP login and registration – send OTP, verify OTP and issue tokens."""



from controllers.user.phone.send_otp import PhoneSendOtpController
from controllers.user.phone.verify_otp import PhoneVerifyOtpController

__all__ = ["PhoneSendOtpController", "PhoneVerifyOtpController"]
