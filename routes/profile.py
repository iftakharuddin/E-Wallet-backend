from flask import Blueprint, request, jsonify, send_file
from services.registration_service import RegistrationService
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from forms.forms import UserUpdateForm
from services.profile import ProfileService
from utils.response_handler import *

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_phone = get_jwt_identity()
    user = RegistrationService.get_user_by_phone(user_phone)
    user_json = {col.name: getattr(user, col.name) for col in user.__table__.columns} if user else None
    return ResponseHandler.generate("S001", data=user_json)

@profile_bp.route("/profile/update", methods=["PATCH"])
@jwt_required()
def profile_update():
    json_data = request.form.get("json_data")  # Extract JSON as string
    data = json.loads(json_data) if json_data else {}
    form = UserUpdateForm(data=data)  # Bind JSON request data to the form

    if form.validate_on_submit():
        user_phone = get_jwt_identity()
        ok = ProfileService.update(user_phone, form)
        return jsonify({"msg": "Profile Updated successfully."}), 200
    return jsonify({"errors": form.errors}), 400

@profile_bp.route("/balance", methods=["GET"])
@jwt_required()
def balance():
    user_phone = get_jwt_identity()
    balance = ProfileService.get_balance_by_phone(user_phone)
    return ResponseHandler.generate("S001", data={"balance": balance})


@profile_bp.route('/download-image', methods=['GET'])
def download_image():
    file_path = 'resources/images/x.png'  # Specify the image or file path here
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e), 400