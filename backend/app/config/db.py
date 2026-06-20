import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Used to sign email-verification / password-reset / delete-account tokens
    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)

    PROPAGATE_EXCEPTIONS = True

    # Brevo (transactional email)
    BREVO_API_KEY = os.getenv("BREVO_API_KEY")
    BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
    BREVO_SENDER_NAME = os.getenv("BREVO_SENDER_NAME", "Fountain of Fire Ministry")

    # Base URL of the deployed frontend, used to build links inside emails
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5500")

    # Token expiry windows (seconds)
    EMAIL_VERIFICATION_MAX_AGE = 60 * 60 * 24       # 24 hours
    PASSWORD_RESET_MAX_AGE = 60 * 60                # 1 hour
    ACCOUNT_DELETE_MAX_AGE = 60 * 60                # 1 hour
