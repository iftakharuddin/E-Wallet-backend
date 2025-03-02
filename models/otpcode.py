from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from extensions import db

class OTPCode(db.Model):
    __tablename__ = "OTP_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Reference to users table
    otp_code = Column(String(6), nullable=False)  # 6-digit OTP
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, user_id, otp_code, expires_at):
        self.user_id = user_id
        self.otp_code = otp_code
        self.expires_at = expires_at
