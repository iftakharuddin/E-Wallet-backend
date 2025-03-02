from flask import Blueprint, request, jsonify
from services.registration_service import RegistrationService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, unset_refresh_cookies
from utils.response_handler import *
from forms.forms import *
from exceptions.exception_class import *


signin_bp = Blueprint("signin", __name__)

@signin_bp.route("/signin", methods=["POST"])
def signin():
    form = SignInForm()
    if not form.validate_on_submit():
        raise InvalidInput(form.errors)

    data = request.json
    phone = data.get("phone")
    pin = data.get("pin")

    user = RegistrationService.get_user_by_phone(phone)

    if user and user.password_hash == pin:
        access_token = create_access_token(identity=str(user.phone))
        refresh_token = create_refresh_token(identity=str(user.phone))
        response = ResponseHandler.generate("S001", data={"access_token": access_token, "refresh_token": refresh_token})

        # response = jsonify({"responseCode": "S001", "responseMessage": "Login successful"})
        # set_access_cookies(response, access_token)
        # set_refresh_cookies(response, refresh_token)
        return response
    
    raise InvalidCredentials()


@signin_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_phone = get_jwt_identity()
    return jsonify({"message": "Access granted", "user_phone": user_phone}), 200

# Refresh Token Route - Generate New Access Token
@signin_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Requires a valid refresh token
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)


@signin_bp.route("/logout", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated
def logout():
    response = jsonify({"responseCode": "S001", "responseMessage": "Successfully logged out"})
    # these two line of code is for unset access and refresh token from cookies by setting expire time to past date.
    # unset_jwt_cookies(response)  # Clear JWT cookies
    # unset_refresh_cookies(response)
    return response