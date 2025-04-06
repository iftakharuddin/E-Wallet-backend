from models.linked_bank_account import *
from extensions import db
from app import app

def register_bank(name, client_id, client_secret):
    bank = Bank(
        name=name,
        client_id=client_id,
        client_secret=client_secret
    )
    db.session.add(bank)
    db.session.commit()

    return {"id": bank.id, "name": name}

with app.app_context():
    print(register_bank("Dutch Bangla Bank Limited", 'ef7f9d22-923c-4c8a-8f8d-cc8735e7a2ee', '5c1a41c7b70429bfc6fa12737fdb0062'))