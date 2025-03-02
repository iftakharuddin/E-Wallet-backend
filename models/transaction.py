from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from extensions import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(String(100), nullable=False)
    feature_code = Column(String(50), nullable=False)
    amount = Column(DECIMAL(50, 2), nullable=False)
    receiver = Column(String(100), nullable=False)
    tnxID = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    charge = Column(DECIMAL(10, 2), default=0.0, nullable=False)
    reference = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Transaction(id={self.id}, sender={self.sender}, receiver={self.receiver}, amount={self.amount}, tnxID={self.tnxID})>"
