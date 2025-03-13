import random
import string
from models.transaction import *

def generate_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def generate_unique_transaction_id():
    while True:
        transaction_id = generate_transaction_id()
        existing = Transaction.query.filter_by(tnxID=transaction_id).first()
        if not existing:  # Ensure it's unique
            return transaction_id
    