class EWalletException(Exception):
    def __init__(self, code, message, status_code=400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self):
        return {"responseCode": self.code, "responseMessage": self.message}

class InvalidRequest(EWalletException):
    def __init__(self):
        super().__init__("E001", "Invalid request", 400)

class AuthenticationFailed(EWalletException):
    def __init__(self):
        super().__init__("E002", "Authentication failed", 401)

class InsufficientBalance(EWalletException):
    def __init__(self):
        super().__init__("E003", "Insufficient balance", 400)

class TransactionLimitExceeded(EWalletException):
    def __init__(self):
        super().__init__("E004", "Transaction limit exceeded", 400)

class InternalServerError(EWalletException):
    def __init__(self):
        super().__init__("E005", "Internal server error", 500)

class InvalidInput(EWalletException):
    def __init__(self, error):
        super().__init__("E006", "Invalid Input", 400)
        self.error = error

    def to_dict(self):
        response = super().to_dict()
        response["error"] = self.error
        return response

class InvalidRegistrationNo(EWalletException):
    def __init__(self):
        super().__init__("E007", "Invalid Registration No", 400)

class InvalidOTP(EWalletException):
    def __init__(self):
        super().__init__("E008", "Invalid OTP, should be 6 digits", 400)

class ExpiredOTP(EWalletException):
    def __init__(self):
        super().__init__("E009", "OTP is expired", 400)

class InvalidCredentials(EWalletException):
    def __init__(self):
        super().__init__("E010", "Invalid Credentials", 401)

class InvalidPhoneNumber(EWalletException):
    def __init__(self):
        super().__init__("E011", "Invalid Phone Number, it should be valid format.", 401)

class InvalidSessionID(EWalletException):
    def __init__(self):
        super().__init__("E012", "Invalid sessoin ID", 400)

class IncorrectInfo(EWalletException):
    def __init__(self):
        super().__init__("E013", "Information given is incorrect", 400)

class OTPVerificationRequired(EWalletException):
    def __init__(self):
        super().__init__("E014", "Didn't pass OTP verification. It is required.", 400)

class IncorrectTemporaryPin(EWalletException):
    def __init__(self):
        super().__init__("E015", "Given Temporary Pin is incorrect.", 400)

class TemporaryPinExpired(EWalletException):
    def __init__(self):
        super().__init__("E015", "Temporary Pin Expired.", 400)

class MissingCompletionPrecedingStep(EWalletException):
    def __init__(self):
        super().__init__("E016", "Didn't complete preceding steps. should be complete before proceed.", 400)