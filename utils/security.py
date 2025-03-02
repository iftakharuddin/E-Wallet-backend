from werkzeug.security import generate_password_hash, check_password_hash

class SecurityUtils:
    @staticmethod
    def hash_password(password):
        """Hashes a password using bcrypt."""
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password, hashed_password):
        """Verifies a password hash."""
        return check_password_hash(hashed_password, password)
