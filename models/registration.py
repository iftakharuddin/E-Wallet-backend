from datetime import datetime, timedelta
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, ENUM
from extensions import db
from enum import Enum

class UserType(str, Enum):
    NORMAL = "normal"
    ADMIN = "admin"
    AGENT = "agent"

class Registration(db.Model):
    __tablename__ = "registration"

    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True, nullable=False)
    user_type = Column(ENUM(UserType), nullable=False)
    registration_no = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    mobile_operator = Column(String(10), nullable=False)
    otp = Column(String(6), nullable=True)  # OTP will be stored temporarily
    otp_verified = Column(Boolean, default=False, nullable=False)
    otp_expired_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Registration {self.phone}, OTP Verified: {self.otp_verified}>"
