from flask import Blueprint, request, jsonify
from forms.sendmoney import *
from exceptions.exception_class import *
from services.send_money import *
from utils.response_handler import *
from flask_jwt_extended import *


sendmoney_bp = Blueprint('sendmoney', __name__)

@sendmoney_bp.route("/verify_receiver", methods=["POST"])
@jwt_required()
def verify_receiver():
    form = RecipientForm()

    if not form.validate_on_submit():
        raise InvalidInput(form.errors)
    
    data = request.get_json()
    recipient = data.get("recipient")

    exist = SendMoney.does_user_exist(recipient)

    if not exist:
        raise InvalidRecipient()
    
    return ResponseHandler.generate("S001", data={"msg": "Recipient is valid. Proceed with amount..."})

@sendmoney_bp.route("/verify_amount", methods=["POST"])
@jwt_required()
def verify_amount():
    user_phone = get_jwt_identity()
    
    form = AmountForm()

    if not form.validate_on_submit():
        raise InvalidInput(form.errors)

    data = request.get_json()
    amount = data.get("amount")
    amount = int(amount)

    status = SendMoney.verify_amount(user_phone, amount)

    if status == 1:
        raise InsufficientBalance()
    elif status == 2:
        raise DailyLimitExceeded()
    elif status == 3:
        raise MonthlyLimitExceeded()
    
    charge = SendMoney.calculate_charge(user_phone, amount)

    return ResponseHandler.generate("S001", data={"amount": amount, "charge": charge, "total": amount + charge})

