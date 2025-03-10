from flask import Blueprint, request, jsonify
from forms.sendmoney import *
from exceptions.exception_class import *
from services.send_money import *
from utils.response_handler import *



sendmoney_bp = Blueprint('sendmoney', __name__)

@sendmoney_bp.route("/verify_receiver", methods=["POST"])
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