from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Date, Column, Integer, String, Boolean, DECIMAL, DateTime, Enum as SQLAEnum
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base
from extensions import db
from sqlalchemy.orm import relationship
from models.registration import UserType

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class Status(str, Enum):
    LOCKED = "locked"
    INACTIVE = "inactive"
    ACTIVE = "active"

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(25))
    first_name = Column(String(25))
    last_name = Column(String(25))
    user_type = Column(ENUM(UserType), nullable=False)  # Enum Type
    password_hash = Column(String(100), nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    phone = Column(String(20), unique=True)
    NID_front = Column(String(100))  # Optional
    NID_back = Column(String(100))   # Optional
    photo = Column(String(100))      # Optional
    gender = Column(SQLAEnum(Gender), nullable=False)  # Enum Type
    income_source = Column(String(50))  # Optional
    monthly_income_amount = Column(DECIMAL(20, 2), default=0.00)  # Optional
    designation = Column(String(25))  # Optional
    status = Column(SQLAEnum(Status), nullable=False, default=Status.ACTIVE)  # Enum Type

    account = relationship("Account", back_populates="user")
    dob = Column(Date)

    def __repr__(self):
        return f"<User {self.username}, Type: {self.user_type}, Status: {self.status}>"

