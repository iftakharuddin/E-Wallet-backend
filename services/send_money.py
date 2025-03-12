from models.user import *
from models.limit import *
from models.user_daily_total import *
from models.user_monthly_total import *
from extensions import db


class SendMoney:

    @staticmethod
    def does_user_exist(phone):
        user = User.query.filter_by(phone=phone).first()
        if user:
            return True
        else:
            return False

    @staticmethod
    def verify_amount(user_phone, amount):
        user = User.query.filter_by(phone=user_phone).first()

        balance = user.account[0].balance
        
        if balance - 100 < amount:
            return 1
        
        # checking for daily limit if exceeded or not.
        today_date = datetime.utcnow().date()

        daily_limit = Limit.query.filter_by(feature_code="send_money").first().daily_limit
        user_daily_total = UserDailyTotal.query.filter(
            UserDailyTotal.user_id == user.id
        ).filter(
            UserDailyTotal.date == today_date
        ).filter(
            UserDailyTotal.feature_code == "send_money"
        ).first()

        if not user_daily_total:
            current_daily_total = 0
        else: 
            current_daily_total = user_daily_total.amount

        if amount + current_daily_total > daily_limit:
            return 2
        
        # checking for monthly limit if exceeded or not.
        
        def get_month_year(date):
            return date.strftime("%Y-%m")  # Returns "YYYY-MM"

        today = datetime.utcnow()
        cur_month_year = get_month_year(today)

        monthly_limit = Limit.query.filter_by(feature_code="send_money").first().monthly_limit
        user_monthly_total = UserMonthlyTotal.query.filter(
            UserMonthlyTotal.user_id == user.id
        ).filter(
            UserMonthlyTotal.month_year == cur_month_year
        ).filter(
            UserMonthlyTotal.feature_code == "send_money"
        ).first()

        if not user_monthly_total:
            current_monthly_total = 0
        else:
            current_monthly_total = user_monthly_total.amount
            
        if amount + current_monthly_total > monthly_limit:
            return 3

        return 4

    @staticmethod
    def calculate_charge(user_phone, amount):
        return amount * (2 / 100)
        
        
