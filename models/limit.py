from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from extensions import db

class Limit(db.Model):
    __tablename__ = "limits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    feature_code = Column(String(25), nullable=False, unique=True)
    daily_limit = Column(Numeric(10, 2), nullable=False)  # Assuming it's a decimal value
    monthly_limit = Column(Numeric(10, 2), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Limit(feature_code={self.feature_code}, daily_limit={self.daily_limit}, monthly_limit={self.monthly_limit})>"
