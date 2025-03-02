from flask import Blueprint, request, jsonify
from services.otp_service import *
from services.registration_service import *
from services.send_otp_gateway import *
from utils.check_validity import *
from exceptions.exception_class import *
from utils.response_handler import *
from services.reset_pin_service import *
from forms.forms import *

pin_bp = Blueprint("pin", __name__)

@pin_bp.route('/pin_reset', methods=['POST'])
def send_otp_to_pin_reset():
    data = request.get_json()
    phone = data.get("phone")

    if not is_valid_phone(phone):
        raise InvalidPhoneNumber()

    user = RegistrationService.get_user_by_phone(phone)
    if not user:
        return ResponseHandler.generate("M004")
    
    otp, session_id = PinResetService.send_otp_to_reset_pin(user)

    return ResponseHandler.generate("S001", data={"msg": "OTP is sent via SMS. Proceed with OTP.", "otp": otp, "session_id": session_id})

@pin_bp.route('/pin_reset/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    otp = data.get("otp")
    session_id = data.get("session_id")

    if not valid_otp(otp):
        raise InvalidOTP()
    if not is_valid_uuid(session_id):
        raise InvalidSessionID()
    
    ok = PinResetService.verify_otp(otp, session_id)

    if ok == 0:
        raise InvalidSessionID()
    elif ok == 1:
        raise InvalidOTP()
    elif ok == 2:
        raise ExpiredOTP()
    
    return ResponseHandler.generate("S001", data={"msg": "OTP verification successful"})


@pin_bp.route('/pin_reset/verify_info', methods=['POST'])
def verify_info():
    form = PinResetInfoForm()

    if not form.validate_on_submit():
        raise InvalidInput(form.errors)
    
    data = request.get_json()
    session_id = data.get("session_id")
    tnxs_in_last_3_days = int(data.get("tnxs_in_last_3_days"))
    dob = data.get("dob")

    ok = PinResetService.verify_info(session_id, tnxs_in_last_3_days, dob)

    if ok == 0:
        raise InvalidSessionID()
    elif ok == 1:
        raise OTPVerificationRequired()
    elif ok == 2:
        raise IncorrectInfo()

    temp_pin = PinResetService.send_temporary_pin(session_id)

    return ResponseHandler.generate("S001", data={"temporary_pin": temp_pin, "msg": "Temporary pin is sent via sms. It will be valid for 5 min. In the meantime, you can reset your pin."})


@pin_bp.route('/pin_reset/final', methods=['POST'])
def pin_reset_final():
    form = PinResetFinalForm()

    if not form.validate_on_submit():
        raise InvalidInput(form.errors)

    data = request.get_json()
    session_id = data.get("session_id")
    temp_pin = data.get("temp_pin")
    new_pin = data.get("new_pin")

    ok = PinResetService.pin_reset_final(session_id, temp_pin, new_pin)

    if ok == 0:
        raise InvalidSessionID()
    elif ok == 1:
        raise MissingCompletionPrecedingStep()
    elif ok == 2:
        raise IncorrectTemporaryPin()
    elif ok == 3:
        raise TemporaryPinExpired()
    
    return ResponseHandler.generate("S001", data={"msg": "Pin Reset Successful."})