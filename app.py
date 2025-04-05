from extensions import db
from flask_migrate import Migrate
from flask import Flask, request, jsonify
from flask import session
from flask_wtf.csrf import generate_csrf
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
# import os

# basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config.BaseConfig')

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
jwt = JWTManager(app)
CORS(app)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=16)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

from models.user import User
from models.registration import Registration
from models.otpcode import OTPCode
from models.pin_reset import PinReset
from models.transaction import Transaction

from routes.registration import registration_bp
from routes.signin import signin_bp
from routes.profile import profile_bp
from routes.password import pin_bp
from routes.send_money import sendmoney_bp
from routes.dashboard import dashboard_bp
from routes.link_bank import linkbank_bp
from exceptions.exception_handler import exception_bp


app.register_blueprint(registration_bp)
app.register_blueprint(signin_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(pin_bp)
app.register_blueprint(exception_bp)
app.register_blueprint(sendmoney_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(linkbank_bp)

@app.route("/")
def hello_world():
    return jsonify({"Message": "Welcome!!"})

@app.route('/get-csrf-token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    session['csrf_token'] = token  # Store token in session
    return jsonify({"csrf_token": token})


class InvalidUsage(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {"error": self.message}

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/validate/<int:value>')
def validate(value):
    if value > 0:
        raise InvalidUsage("Value must be non-negative!", 400)
    return jsonify({"value": value})



if __name__=="__main__":
    app.run(debug=True)