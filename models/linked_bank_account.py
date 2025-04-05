import uuid
import datetime
from extensions import db

class LinkedBankAccount(db.Model):
    __tablename__ = "linked_bank_accounts"

    link_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    wallet_id = db.Column(db.String(50), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    bank_link_id = db.Column(db.String(50), nullable=True)  # received from bank
    is_verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(1024), nullable=True)
    bank_id = db.Column(db.Integer, db.ForignKey('banks.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Bank(db.Model):
    __tablename__ = "banks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.String(100), nullable=False)
    client_secret = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(100), nullable=False)