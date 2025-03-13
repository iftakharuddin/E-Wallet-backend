from flask import Blueprint, request, jsonify
from forms.sendmoney import *
from exceptions.exception_class import *
from services.send_money import *
from utils.response_handler import *
from flask_jwt_extended import *


sendmoney_bp = Blueprint('sendmoney', __name__)

@sendmoney_bp.route("/send_money/verify_receiver", methods=["POST"])
@jwt_required()
def verify_receiver():
    form = RecipientForm()

    if not form.validate_on_submit():
        raise InvalidInput(form.errors)
    
    data = request.get_json()
    recipient = data.get("recipient")

    user_phone = get_jwt_identity()
    if user_phone == recipient:
        raise ChooseDifferentAccount()

    exist = SendMoney.does_user_exist(recipient)

    if not exist:
        raise InvalidRecipient()
    
    return ResponseHandler.generate("S001", data={"msg": "Recipient is valid. Proceed with amount..."})

@sendmoney_bp.route("/send_money/verify_amount", methods=["POST"])
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


@sendmoney_bp.route("/send_money/final", methods=["POST"])
@jwt_required()
def send_money_final():
    form = SendMoneyForm()

    if not form.validate_on_submit():
        raise InvalidInput(form.errors)
    
    data = request.get_json()
    recipient = data.get("recipient")
    amount = int(data.get("amount"))
    ref = data.get("reference")
    idempotency_key = data.get("idempotency_key")
    user_phone = get_jwt_identity()
    
    exist = SendMoney.get_tnx_by_idempotency_key(idempotency_key)
    if exist:
        return ResponseHandler.generate("S001", data={"tnxId": exist.tnxID, "charge": exist.charge, "time": exist.created_at})

    if user_phone == recipient:
        raise ChooseDifferentAccount()

    exist = SendMoney.does_user_exist(recipient)

    if not exist:
        raise InvalidRecipient()
    
    status = SendMoney.verify_amount(user_phone, amount)

    if status == 1:
        raise InsufficientBalance()
    elif status == 2:
        raise DailyLimitExceeded()
    elif status == 3:
        raise MonthlyLimitExceeded()
    
    tnxId, charge, time = SendMoney.send_money(user_phone, amount, recipient, idempotency_key, ref)

    return ResponseHandler.generate("S001", data={"tnxId": tnxId, "charge": charge, "time": time})