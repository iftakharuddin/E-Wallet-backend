from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

class RecipientForm(FlaskForm):
    recipient = StringField("Recipient", validators=[
        DataRequired(message="Recipient Phone is required."),
        Regexp(r'^(?:\+8801[3-9]\d{8}|01[3-9]\d{8})$', message="Recipient phone must be valid and of the format starting with 01*********")
    ])

class AmountForm(FlaskForm):
    amount = StringField("Amount", validators=[
        DataRequired(message="Amount is required."),
        Regexp(r'\d+', message="Amount must be a valid number.")
    ])

class SendMoneyForm(FlaskForm):
    recipient = StringField("Recipient", validators=[
        DataRequired(message="Recipient Phone is required."),
        Regexp(r'^(?:\+8801[3-9]\d{8}|01[3-9]\d{8})$', message="Recipient phone must be valid and of the format starting with 01*********")
    ])
    amount = StringField("Amount", validators=[
        DataRequired(message="Amount is required."),
        Regexp(r'\d+', message="Amount must be a valid number.")
    ])
    reference = StringField("Reference", validators=[
        DataRequired(), Length(max=100)
    ])
    idempotency_key = StringField("Idempotency Key",  validators=[
        DataRequired(message="Idempotency key is required."),
        Length(min=10, max=20, message="Idempotency key must be min 10, max20 characters long."),
        Regexp(r"^[a-zA-Z0-9]{10,20}$", message="Idempotency key must be alphanumeric.")
    ])