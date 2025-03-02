from flask import jsonify

class ResponseHandler:
    # Predefined response codes and messages
    RESPONSE_CODES = {
        "S001": "Successful",
        "S002": "Sign up successful",
        # "E001": "Invalid request",
        # "E002": "Authentication failed",
        # "E003": "Insufficient balance",
        # "E004": "Transaction limit exceeded",
        # "E005": "Internal server error",
        # "E006": "Invalid Input",
        "M001": "Phone number already registered",
        "M002": "OTP verification must be needed",
        "M003": "User already registered",
        "M004": "There is no account against this number.",
        # "E007": "Invalid Registration No",
        # "E008": "Invalid OTP, should be 6 digits",
        # "E009": "OTP is expired",
        "E500": "An unexpected error occurred"
    }

    @staticmethod
    def generate(response_code, data=None):
        """
        Generate a standardized JSON response.

        :param response_code: The response code (e.g., "S001")
        :param data: The actual data to be returned (default: None)
        :return: Flask JSON response
        """
        response_message = ResponseHandler.RESPONSE_CODES.get(response_code, "Unknown response code")
        response_body = {
            "responseCode": response_code,
            "responseMessage": response_message,
            "data": data
        }
        return jsonify(response_body), 200 if response_code.startswith("S") else 400  # Success -> 200, Error -> 400
