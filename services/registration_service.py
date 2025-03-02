from models.registration import Registration
from models.user import User
from models.account import Account
from extensions import db
from utils.check_validity import is_valid_uuid
import uuid
from werkzeug.utils import secure_filename
import os
from flask import current_app
from datetime import datetime

class RegistrationService:
    @staticmethod
    def create_registration(phone, user_type, mobile_operator):
        """Creates a new registration entry and returns registration_no."""
        registration = Registration(
            phone=phone,
            user_type=user_type,
            mobile_operator=mobile_operator,
        )
        db.session.add(registration)
        db.session.commit()
        return registration

    @staticmethod
    def get_registration_by_rno(registration_no):
        """Fetches a registration record by registration_no."""

        if not is_valid_uuid(registration_no):
            return None
        return Registration.query.filter_by(registration_no=registration_no).first()

    
    @staticmethod
    def get_registration_by_phone(phone):
        """Fetches a registration record by phone."""
        return Registration.query.filter_by(phone=phone).first()
    @staticmethod
    def get_user_by_phone(phone):
        """Fetches a user record by phone."""
        return User.query.filter_by(phone=phone).first()
    @staticmethod
    def create_user(form, data):
        registration_no = data.get("registration_no")
        registration = RegistrationService.get_registration_by_rno(registration_no)
        user = RegistrationService.get_user_by_phone(registration.phone)
        if user:
            return False, user
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        username = data.get("username")
        pin = data.get("pin")
        confirm_pin = data.get("confirm_pin")
        gender = data.get("gender")
        income_source = data.get("income_source")
        monthly_income_amount = data.get("monthly_income_amount")
        designation = data.get("designation")
        dob = datetime.strptime(data.get("dob"), "%Y-%m-%d").date()

        upload_folder = current_app.config['UPLOAD_FOLDER']
        NIDfrontfilename = RegistrationService.save_file(form.NIDfront.data, upload_folder)
        NIDbackfilename = RegistrationService.save_file(form.NIDback.data, upload_folder)
        picfilename = RegistrationService.save_file(form.user_pic.data, upload_folder)

        user = User(
            username=username,
            first_name=firstname,
            last_name=lastname,
            user_type=registration.user_type,
            password_hash=pin,
            verified=True,
            phone=registration.phone,
            NID_front=NIDfrontfilename,
            NID_back=NIDbackfilename,
            photo=picfilename,
            gender=gender,
            income_source=income_source,
            monthly_income_amount=monthly_income_amount,
            designation=designation,
            status="active",
            dob=dob
        )
        db.session.add(user)
        db.session.commit()
        return True, user

    @staticmethod
    def save_file(file, upload_folder):
        if file:
            # Generate a unique filename using UUID
            unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}"
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            return unique_filename
        return None

    @staticmethod
    def create_account(user_id):
        if not user_id:
            return False, None

        account = Account(
            user_id=user_id
        )
        db.session.add(account)
        db.session.commit()
        return True, account