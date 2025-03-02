from models.user import User
from models.account import Account
from services.registration_service import RegistrationService
from extensions import db
import os
from flask import current_app


class ProfileService:
    @staticmethod
    def update(phone, form):
        user = RegistrationService.get_user_by_phone(phone)
        if not user:
            return False

        user.first_name = form.firstname.data
        user.last_name = form.lastname.data
        user.username = form.username.data

        user.gender = form.gender.data
        user.income_source = form.income_source.data
        user.monthly_income_amount = form.monthly_income_amount.data
        user.designation=form.designation.data

        upload_folder = current_app.config['UPLOAD_FOLDER']
        ProfileService.delete_image(upload_folder, user.NID_front)
        ProfileService.delete_image(upload_folder, user.NID_back)
        ProfileService.delete_image(upload_folder, user.photo)

        NIDfrontfilename = RegistrationService.save_file(form.NIDfront.data, upload_folder)
        NIDbackfilename = RegistrationService.save_file(form.NIDback.data, upload_folder)
        picfilename = RegistrationService.save_file(form.user_pic.data, upload_folder)

        user.NID_front = NIDfrontfilename
        user.NID_back = NIDbackfilename
        user.photo = picfilename

        db.session.commit()
        return True


    @staticmethod
    def get_balance_by_phone(user_phone):
        user = User.query.filter_by(phone=user_phone).first()
        return user.account[0].balance

    @staticmethod
    def delete_image(path, image_name):
        file_path = os.path.join(path, image_name)

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except:
                return False
        return False