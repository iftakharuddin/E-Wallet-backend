import random
from datetime import datetime, timedelta
from models.registration import Registration
from extensions import db
from services.send_otp_gateway import SendOTPGateway
from services.registration_service import RegistrationService
from models.otpcode import *

class OTPService:

    @staticmethod
    def generate_otp():
        """Generates a 6-digit OTP"""
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_otp(sog: SendOTPGateway):
        """Generates and stores OTP for a user"""

        registration = RegistrationService.get_registration_by_rno(sog.recipient)

        if not registration:
            return None
        otp = OTPService.generate_otp()
        registration.otp = otp
        registration.otp_expired_at = datetime.utcnow() + timedelta(minutes=5)
        db.session.commit()

        # code to sending otp via sms
        sog.send_otp(otp)

        return otp  # ⚠️ Remove OTP from response in production

    @staticmethod
    def verify_otp(otp, registration_no):
        registration = RegistrationService.get_registration_by_rno(registration_no)
        if not registration:
            return None

        current_time = datetime.utcnow()
        if registration.otp != otp or current_time > registration.otp_expired_at:
            return False
        registration.otp_verified = True
        db.session.commit()
        return True

    @staticmethod
    def send_otp_general(user, sog: SendOTPGateway):
        if not user:
            return None

        old_otp = OTPCode.query.filter_by(user_id=user.id).first()
        if old_otp:
            db.session.delete(old_otp)
            db.session.commit()

        otp = OTPService.generate_otp()
        
        new_otp = OTPCode(
            user_id = user.id,
            otp_code = otp,
            expires_at = datetime.utcnow() + timedelta(minutes=5)
        )
        db.session.add(new_otp)
        db.session.commit()

        sog.send_otp(otp)

        return otp