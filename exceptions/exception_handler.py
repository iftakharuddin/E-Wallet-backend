import logging
import traceback
from flask import Blueprint, jsonify
from utils.response_handler import *
from exceptions.exception_class import EWalletException

# Create a Blueprint for handling exceptions
exception_bp = Blueprint('exception', __name__)

@exception_bp.app_errorhandler(Exception)
def handle_general_exception(error):
    # Capture the full traceback
    error_traceback = traceback.format_exc()

    # Log detailed error information
    logging.error(f"Unhandled Exception: {error}\nTraceback:\n{error_traceback}")
    return ResponseHandler.generate("E500")

@exception_bp.app_errorhandler(EWalletException)
def handle_ewallet_exception(error):
    """Handle custom EWalletException errors."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@exception_bp.app_errorhandler(404)
def handle_404(error):
    """Handle 404 errors (Not Found)."""
    return jsonify({"responseCode": "E404", "responseMessage": "Resource not found"}), 404

@exception_bp.app_errorhandler(500)
def handle_500(error):
    """Handle 500 errors (Internal Server Error)."""
    return jsonify({"responseCode": "E500", "responseMessage": "Internal Server Error"}), 500


