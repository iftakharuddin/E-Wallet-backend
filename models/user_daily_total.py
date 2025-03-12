from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from extensions import db

class UserDailyTotal(db.Model):
    __tablename__ = "user_daily_total"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False, default=datetime.utcnow().date())
    amount = Column(Numeric(10, 2), nullable=False)  # Storing as decimal value
    feature_code = Column(String(25), nullable=False)

    def __repr__(self):
        return f"<UserDailyTotal(user_id={self.user_id}, date={self.date}, amount={self.amount}, feature_code={self.feature_code})>"
