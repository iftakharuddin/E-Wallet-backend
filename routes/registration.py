from flask import Blueprint, request, jsonify
from services.registration_service import RegistrationService
from services.otp_service import OTPService
from models.user import User
from services.send_otp_gateway import EmailGateway
import json
from forms.forms import UserForm, RegistrationForm
from utils.serialize import serialize_form_data
from utils.response_handler import *
from utils.check_validity import *
from exceptions.exception_handler import *
from exceptions.exception_class import *

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/signup/start', methods=['POST'])
def start_registration():

    form = RegistrationForm()

    if not form.validate_on_submit():
        raise InvalidInput(form.errors)
        # return ResponseHandler.generate(response_code="E006", data=form.errors)
    # Check if user is already registered

    data = request.get_json()
    user_type = data.get("user_type")
    phone = data.get("phone")
    mobile_operator = data.get("mobile_operator")

    existing_user = User.query.filter_by(phone=phone).first()
    if existing_user:
        return ResponseHandler.generate(response_code="M001")

    # Check if there's a pending registration
    pending = RegistrationService.get_registration_by_phone(phone)
    
    if not pending:
        pending = RegistrationService.create_registration(phone, user_type, mobile_operator)

    otp = OTPService.send_otp(EmailGateway(pending.registration_no))

    return ResponseHandler.generate(response_code="S001", data={
        "registration_no": pending.registration_no,
        "OTP": otp
    })


@registration_bp.route('/signup/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    registration_no = data.get("registration_no")

    if not is_valid_uuid(registration_no):
        raise InvalidRegistrationNo()

    otp = OTPService.send_otp(EmailGateway(registration_no))
    
    return ResponseHandler.generate(response_code="S001", data={"message": "OTP is sent", "otp": otp})  # ⚠️ Remove OTP in production


@registration_bp.route('/signup/verify_otp', methods={'POST'})
def verify_otp():
    data = request.get_json()
    otp = data.get("otp")
    registration_no = data.get("registration_no")
    print(data)
    if not valid_otp(otp):
        raise InvalidOTP()
    if not is_valid_uuid(registration_no):
        raise InvalidRegistrationNo()

    ok = OTPService.verify_otp(otp, registration_no)
    print(ok)
    if not ok:
        raise WrongOrExpiredOTP()
    print("1")
    return ResponseHandler.generate("S001", data={"msg": "OTP verification successful"})



@registration_bp.route("/signup/final", methods=["POST"])
def register_final():
    # print("JSON Data:", request.get_json())  # Debugging
    json_data = request.form.get("json_data")  # Extract JSON as string
    data = json.loads(json_data) if json_data else {}
    form = UserForm(data=data)  # Bind JSON request data to the form

    if form.validate_on_submit():
        registration = data.get("registration_no")
        if not is_valid_uuid(registration):
            raise InvalidRegistrationNo()
        registration = RegistrationService.get_registration_by_rno(data.get("registration_no"))
        if not registration:
            raise InvalidRegistrationNo()
        if not registration.otp_verified:
            return ResponseHandler.generate("M002")

        user_created, user = RegistrationService.create_user(form, data)
        if not user_created: 
            return ResponseHandler.generate("M003")
        account_created, account = RegistrationService.create_account(user.id)
        return ResponseHandler.generate("S002", data={"info": serialize_form_data(form), "balance": account.balance})
    else:
        raise InvalidInput(form.errors) # Return validation errors


