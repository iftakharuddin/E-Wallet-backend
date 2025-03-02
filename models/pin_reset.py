from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
import uuid
from extensions import db
from sqlalchemy.orm import relationship

class PinReset(db.Model):
    __tablename__ = "pin_reset"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Assuming users table exists
    session_id = Column(PG_UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True)
    otp_code = Column(String(6), nullable=False)  # 6-digit OTP
    otp_expires_at = Column(DateTime, nullable=False)
    step_done = Column(Integer, nullable=False, default=0)  # Steps: 0, 1, 2, 3
    temp_pin = Column(String(10), nullable=True)  # Assuming PIN is alphanumeric
    temp_pin_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")

    def __repr__(self):
        return f"<PinReset user_id={self.user_id} session_id={self.session_id} step={self.step_done}>"
