from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, validators, IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, Regexp, NumberRange, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from utils.custom_validators import *

class UserForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired(message="First name is required")])
    lastname = StringField("Last Name", validators=[DataRequired(message="Last name is required")])
    username = StringField("Username", validators=[DataRequired(message="Username is required")])
    
    pin = StringField("PIN", validators=[
        DataRequired(message="PIN is required"),
        Regexp(r'^\d{4,6}$', message="PIN must be 4 to 6 digits")
    ])
    
    confirm_pin = StringField("Confirm PIN", validators=[
        DataRequired(message="Confirm PIN is required"),
        EqualTo("pin", message="PIN and Confirm PIN must match")
    ])
    
    gender = StringField("Gender", validators=[
        DataRequired(message="Gender is required"),
        Regexp(r'^(male|female|other)$', message="Gender must be 'male', 'female', or 'other'")
    ])
    
    income_source = StringField("Income Source", validators=[DataRequired(message="Income source is required")])
    monthly_income_amount = FloatField("Monthly Income Amount", validators=[DataRequired(message="Monthly income is required")])
    designation = StringField("Designation", validators=[DataRequired(message="Designation is required")])
    NIDfront = FileField("NID front", validators=[
        FileRequired(message="NID front is required!"),
        FileAllowed(["jpg", "png", "jpeg"], message="Only JPG, PNG, and JPEG files are allowed!"),
        file_size_limit,  # Custom file size validator
        image_dimension_limit  # Custom dimension validator
    ])
    NIDback = FileField("NID back", validators=[
        FileRequired(message="NID front is required!"),
        FileAllowed(["jpg", "png", "jpeg"], message="Only JPG, PNG, and JPEG files are allowed!"),
        file_size_limit,  # Custom file size validator
        image_dimension_limit  # Custom dimension validator
    ])
    user_pic = FileField("User Picture", validators=[
        FileRequired(message="Your picture is required!"),
        FileAllowed(["jpg", "png", "jpeg"], message="Only JPG, PNG, and JPEG files are allowed!"),
        file_size_limit,  # Custom file size validator
        image_dimension_limit  # Custom dimension validator
    ])
    dob = DateField("dob", format="%Y-%m-%d", validators=[DataRequired()])

class UserUpdateForm(UserForm):
    """This form is used when updating user details without PIN validation."""
    pin = StringField("PIN")  # No validators
    confirm_pin = StringField("Confirm PIN")  # No validators

class RegistrationForm(FlaskForm):
    user_type = StringField("User Type", validators=[
        DataRequired(message="User type is required."),
        Regexp(r'^(normal|agent|admin)$', message="User type must be 'normal', 'agent', or 'admin")
    ])
    phone = StringField("Phone", validators=[
        DataRequired(message="Phone is required."),
        Regexp(r'^(?:\+8801[3-9]\d{8}|01[3-9]\d{8})$', message="Phone must be valid and of the format starting with +8801********* or 01*********")
    ])

    mobile_operator = IntegerField("Mobile Operator", validators=[DataRequired(), NumberRange(min=3, max=9)])
    
class SignInForm(FlaskForm):
    phone = StringField("Phone", validators=[
        DataRequired(message="Phone is required."),
        Regexp(r'^(?:\+8801[3-9]\d{8}|01[3-9]\d{8})$', message="Phone must be valid and of the format starting with +8801********* or 01*********")
    ])

    pin = StringField("PIN", validators=[
        DataRequired(message="PIN is required"),
        Regexp(r'^\d{4,6}$', message="PIN must be 4 to 6 digits")
    ])

class PinResetInfoForm(FlaskForm):
    tnxs_in_last_3_days = StringField("tnxs_in_last_3_days", validators=[InputRequired(), Regexp(r"^\d+$", message="Number of Transaction should be a non-negative number in string format.")])
    dob = DateField("dob", format="%Y-%m-%d", validators=[DataRequired()])
    session_id = StringField("session_id", validators=[
    DataRequired(),
    Regexp(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", 
           message="Invalid UUID format")
    ])

class PinResetFinalForm(FlaskForm):
    session_id = StringField("session_id", validators=[
    DataRequired(),
    Regexp(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", 
           message="Invalid UUID format")
    ])

    temp_pin = StringField("PIN", validators=[
        DataRequired(message="Temporary PIN is required"),
        Regexp(r'^\d{6}$', message="Temporary PIN must be 6 digits")
    ])

    new_pin = StringField("PIN", validators=[
        DataRequired(message="PIN is required"),
        Regexp(r'^\d{6}$', message="PIN must be 6 digits")
    ])
    
    confirm_pin = StringField("Confirm PIN", validators=[
        DataRequired(message="Confirm PIN is required"),
        EqualTo("new_pin", message="New PIN and Confirm PIN must match")
    ])