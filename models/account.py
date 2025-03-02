from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from extensions import db

class Account(db.Model):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship (assuming there's a User model)
    user = relationship("User", back_populates="account")  # Adjust User model accordingly

    def __repr__(self):
        return f"<Account(id={self.id}, user_id={self.user_id}, balance={self.balance})>"
