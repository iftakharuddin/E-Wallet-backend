import os
from decouple import config

class BaseConfig:
    """Base configuration."""

    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # "postgresql://todo_database_nbtl_user:GWGBKGmvWYupjzXqnLNpATMCp9u9oiIT@dpg-cug7ne56l47c739vkou0-a/todo_database_nbtl"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:123456@localhost:5432/postgres"
    )
    
    SECRET_KEY = 'bdeaef2749a1a42ee8aee7f5ae2bf8a6020acb7915ac8e49facd3bfa237e4b62'
    SECURITY_PASSWORD_SALT = config("SECURITY_PASSWORD_SALT", default="very-important")
    
    JWT_SECRET_KEY = "mysecretkey"
    # JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT = False

    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = "resources/images"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False