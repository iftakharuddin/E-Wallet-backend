from models.user import *
from extensions import db


class SendMoney:

    @staticmethod
    def does_user_exist(phone):
        user = User.query.filter_by(phone=phone).first()
        print(user)
        if user:
            return True
        else:
            return False