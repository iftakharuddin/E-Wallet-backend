from uuid import UUID
import re

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(str(uuid_to_test), version=version)
    except ValueError :
        return False
    return str(uuid_obj) == str(uuid_to_test)

def valid_otp(otp):
    otp_regex = re.compile(r'^\d{6}$')
    return bool(otp_regex.match(otp))

def is_valid_phone(phone):
    phone_regex = re.compile(r'^(?:\+8801[3-9]\d{8}|01[3-9]\d{8})$')
    return bool(phone_regex.match(phone))
    
