from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transaction import *
from utils.response_handler import *

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/transactions", methods=["GET"])
@jwt_required()
def transactions():
    user_phone = get_jwt_identity()
    transactions_send = Transaction.query.filter_by(sender=user_phone).all()
    transactions_recv = Transaction.query.filter_by(receiver=user_phone).all()

    transactions_json = [
        {**transaction.to_dict(), "transaction_type": "sent"} for transaction in transactions_send
    ] + [
        {**transaction.to_dict(), "transaction_type": "received"} for transaction in transactions_recv
    ]
    return ResponseHandler.generate("S001", data=transactions_json)

