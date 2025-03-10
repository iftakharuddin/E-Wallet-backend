from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

class RecipientForm(FlaskForm):
    recipient = StringField("Recipient", validators=[
        DataRequired(message="Recipient Phone is required."),
        Regexp(r'^(?:\+8801[3-9]\d{8}|01[3-9]\d{8})$', message="Recipient phone must be valid and of the format starting with 01*********")
    ])