from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from extensions import db


class UserMonthlyTotal(db.Model):
    __tablename__ = "user_monthly_total"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key reference
    month_year = Column(String(7), nullable=False)  # Format: "YYYY-MM"
    amount = Column(Numeric(10, 2), nullable=False)
    feature_code = Column(String(25), nullable=False)

    def __repr__(self):
        return f"<UserMonthlyTotal(user_id={self.user_id}, month_year={self.month_year}, amount={self.amount}, feature_code={self.feature_code})>"
