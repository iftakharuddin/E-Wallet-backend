from services.otp_service import *
from datetime import datetime, timedelta
from models.pin_reset import *
from extensions import *
from services.send_otp_gateway import *
from models.transaction import *

class PinResetService:

    @staticmethod
    def generate_pin():
        """Generates a 6-digit PIN"""
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_otp_to_reset_pin(user):

        PinReset.query.filter_by(user_id=user.id).delete()
        db.session.commit()

        otp = OTPService.generate_otp()
        otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
        step_done = 0

        new_row = PinReset(
            user_id = user.id,
            otp_code = otp,
            otp_expires_at = otp_expires_at,
            step_done = 0
        )

        db.session.add(new_row)
        db.session.commit()

        sg = SmsGateway(user)
        sg.send_otp(otp)

        return otp, new_row.session_id

    @staticmethod
    def verify_otp(otp, session_id):
        pin_reset = PinReset.query.filter_by(session_id=session_id).first()
        if not pin_reset:
            return 0
        
        if pin_reset.otp_code != otp:
            return 1
        
        current_time = datetime.utcnow()
        if current_time > pin_reset.otp_expires_at:
            return 2
        
        pin_reset.step_done = 1
        db.session.commit()
        return 3

    @staticmethod
    def verify_info(session_id, number_of_tnxs, dob):
        pin_reset_row = PinReset.query.filter_by(session_id=session_id).first()

        if not pin_reset_row:
            return 0
        
        if pin_reset_row.step_done < 1:
            return 1
        
        dob = datetime.strptime(dob, "%Y-%m-%d").date()

        three_days_ago = datetime.utcnow() - timedelta(days=3)

        # Query to count transactions in the last 3 days for the user
        transaction_count = (
            Transaction.query
            .filter(Transaction.sender == str(pin_reset_row.user_id))
            .filter(Transaction.created_at >= three_days_ago)
            .count()
        )

        if pin_reset_row.user.dob != dob or abs(number_of_tnxs - transaction_count) > 2:
            return 2

        return 3
        
    @staticmethod
    def send_temporary_pin(session_id):
        pin_reset_row = PinReset.query.filter_by(session_id=session_id).first()
        
        pin_reset_row.temp_pin = PinResetService.generate_pin()
        pin_reset_row.temp_pin_expires_at = datetime.utcnow() + timedelta(minutes=5)
        pin_reset_row.step_done = 2
        db.session.commit()

        sg = SmsGateway(pin_reset_row.user)
        sg.send_otp(pin_reset_row.temp_pin)

        return pin_reset_row.temp_pin

    @staticmethod
    def pin_reset_final(session_id, temp_pin, new_pin):
        pin_reset_row = PinReset.query.filter_by(session_id=session_id).first()

        if not pin_reset_row:
            return 0
        
        if pin_reset_row.step_done < 2:
            return 1
        
        if pin_reset_row.temp_pin != temp_pin:
            return 2
        current_time = datetime.utcnow()
        if current_time > pin_reset_row.temp_pin_expires_at:
            return 3

        pin_reset_row.user.password_hash = new_pin
        db.session.commit()
        
        db.session.delete(pin_reset_row)
        db.session.commit()
        
        return 4