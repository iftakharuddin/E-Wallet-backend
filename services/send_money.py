from models.user import *
from models.limit import *
from models.user_daily_total import *
from models.user_monthly_total import *
from models.transaction import *
from extensions import db
from utils.generate_tnxId import *
from exceptions.exception_class import *


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
        
    @staticmethod
    def send_money(sender, amount, recipient, idmkey, ref):
        sender_user = User.query.filter_by(phone=sender).first()
        recipient_user = User.query.filter_by(phone=recipient).first()

        charge = SendMoney.calculate_charge(sender, amount)
        tnxId = generate_unique_transaction_id()

        sender_user.account[0].balance -= amount + charge
        recipient_user.account[0].balance += amount

        transaction = Transaction(
            sender=sender,
            feature_code="send_money",
            amount=amount,
            receiver=recipient,
            tnxID=tnxId,
            charge=charge,
            reference=ref,
            idempotency_key=idmkey
        )

        db.session.add(transaction)
        db.session.commit()

        time = transaction.created_at
        # Update daily total, montyly total 
        SendMoney.add_to_daily_total(sender_user.id, time, amount, "send_money")
        SendMoney.add_to_monthly_total(sender_user.id, time, amount, "send_money")

        return tnxId, charge, time
    
    @staticmethod
    def get_tnx_by_idempotency_key(idempotency_key):
        existing_tnx = Transaction.query.filter_by(idempotency_key = idempotency_key).first()
        return existing_tnx
    
    @staticmethod
    def add_to_daily_total(sender_id, time, amount, feature_code):
        date = time.date()
        user_daily_total = UserDailyTotal.query.filter(
            UserDailyTotal.user_id == sender_id
        ).filter(
            UserDailyTotal.date == date
        ).filter(
            UserDailyTotal.feature_code == feature_code
        ).first()

        if user_daily_total:
            user_daily_total.amount += amount
        else: 
            user_daily_total = UserDailyTotal(
                user_id = sender_id,
                date = date,
                amount = amount,
                feature_code = feature_code
            )
            db.session.add(user_daily_total)
        
        db.session.commit()

    @staticmethod
    def add_to_monthly_total(sender_id, time, amount, feature_code):
        def get_month_year(date):
            return date.strftime("%Y-%m")  # Returns "YYYY-MM"

        month_year = get_month_year(time)

        user_monthly_total = UserMonthlyTotal.query.filter(
            UserMonthlyTotal.user_id == sender_id
        ).filter(
            UserMonthlyTotal.month_year == month_year
        ).filter(
            UserMonthlyTotal.feature_code == feature_code
        ).first()

        if user_monthly_total:
            user_monthly_total.amount += amount
        else: 
            user_monthly_total = UserMonthlyTotal(
                user_id = sender_id,
                month_year = month_year,
                amount = amount,
                feature_code = feature_code
            )
            db.session.add(user_monthly_total)
        
        db.session.commit()
    
    
