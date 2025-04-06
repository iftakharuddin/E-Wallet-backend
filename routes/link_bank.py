from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import *
from models.account import *
from models.linked_bank_account import *
from utils.response_handler import *
import requests

linkbank_bp = Blueprint("linkbank", __name__)

@linkbank_bp.route("/linkbank/banklist", methods=["GET"])
@jwt_required()
def linkbank_list():
    banks = Bank.query.all()
    banksinfo = []
    for bank in banks:
        banksinfo.append({"id": bank.id, "name": bank.name})
    return ResponseHandler.generate("S001", data=banksinfo)

@linkbank_bp.route("/linkbank/start", methods=["POST"])
@jwt_required()
def linkbank_start():
    user_phone = get_jwt_identity()
    data = request.get_json()
    owner = data.get("account_name")
    account_no = data.get("account_no")
    bank_id = data.get("bank_id")
    
    user = User.query.filter_by(phone=user_phone).first()
    wallet_acc = Account.query.filter_by(user_id=user.id).first()
    wallet_id = str(wallet_acc.id)
    
    bank = Bank.query.filter_by(id=bank_id).first()
    if not bank: 
        return jsonify({"message": "Bank doesn't exist."}), 400

    try: 
        response = requests.post("http://localhost:3000/api/verify_bank_account", json={
            "owner": owner,
            "bank_account_number": account_no,
            "wallet_id": wallet_id
        })
        result = response.json()
    except Exception as e:
        return jsonify({"message": "Bank system not responding", "error": str(e)}), 500

    if response.status_code != 200:
        return jsonify(result), 400

    # 2. Save to wallet DB
    bank_link_id = result.get("data").get("link_id")
    # print(bank_link_id)
    linked = LinkedBankAccount(
        wallet_id=wallet_id,
        bank_id=bank_id,
        account_number=account_no,
        owner=owner,
        bank_link_id=bank_link_id,
    )
    db.session.add(linked)
    db.session.commit()

    return ResponseHandler.generate("S001", data={
        "message": "Bank account verification started. OTP sent to user.",
        "link_id": linked.link_id
    })

@linkbank_bp.route("/linkbank/end", methods=["POST"])
@jwt_required()
def linkbank_end():
    user_phone = get_jwt_identity()
    data = request.get_json()
    link_id = data.get("link_id")
    otp = data.get("otp")

    linked_account = LinkedBankAccount.query.filter_by(link_id=link_id).first()

    if not linked_account:
        return jsonify({"message": "Linked account not found"}), 404
    
    bank_link_id = linked_account.bank_link_id

    try:
        response = requests.post("http://localhost:3000/api/verify_otp_link_bank", json={
            "link_id": bank_link_id,
            "otp": otp
        })
        result = response.json()
    except Exception as e:
        return jsonify({"message": "Bank system not responding", "error": str(e)}), 500

    if response.status_code != 200:
        return jsonify(result), 400
    
    token = result.get("data").get("token")
    linked_account.token = token
    linked_account.is_verified = True
    db.session.commit()

    return ResponseHandler.generate("S001", data={"message": "Bank account linked successfully."})