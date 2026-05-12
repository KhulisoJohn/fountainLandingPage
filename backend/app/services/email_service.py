import requests
import os
from app.utils.logger import logger


class EmailService:

    BASE_URL = "https://api.brevo.com/v3/smtp/email"
    API_KEY = os.getenv("BREVO_API_KEY")

    @staticmethod
    def _send_email(payload):

        headers = {
            "accept": "application/json",
            "api-key": EmailService.API_KEY,
            "content-type": "application/json"
        }

        try:
            response = requests.post(
                EmailService.BASE_URL,
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code not in [200, 201, 202]:
                logger.error(f"EMAIL_FAILED | status={response.status_code} | response={response.text}")
                return False

            logger.info("EMAIL_SENT_SUCCESS")
            return True

        except Exception as e:
            logger.error(f"EMAIL_EXCEPTION | error={str(e)}")
            return False


    # ---------------- WELCOME EMAIL ----------------
    @staticmethod
    def send_welcome_email(to_email, name):

        payload = {
            "sender": {
                "name": "Fountain Ministry SA",
                "email": "no-reply@fountainministrysa.net"
            },
            "to": [
                {
                    "email": to_email,
                    "name": name
                }
            ],
            "subject": "Welcome to Fountain Ministry SA 🙏",
            "htmlContent": f"""
                <h2>Welcome {name}</h2>
                <p>Thank you for joining Fountain Ministry SA.</p>
                <p>You are now part of our community.</p>
                <br>
                <p>God bless you 🙏</p>
            """
        }

        return EmailService._send_email(payload)


    # ---------------- VERIFY EMAIL ----------------
    @staticmethod
    def send_verification_email(to_email, token):

        payload = {
            "sender": {
                "name": "Fountain Ministry SA",
                "email": "no-reply@fountainministrysa.net"
            },
            "to": [
                {"email": to_email}
            ],
            "subject": "Verify Your Account",
            "htmlContent": f"""
                <h2>Email Verification</h2>
                <p>Please verify your account by clicking below:</p>
                <a href="http://localhost:5000/api/auth/verify/{token}">
                    Verify Account
                </a>
            """
        }

        return EmailService._send_email(payload)


    # ---------------- RESET PASSWORD ----------------
    @staticmethod
    def send_reset_password_email(to_email, token):

        payload = {
            "sender": {
                "name": "Fountain Ministry SA",
                "email": "no-reply@fountainministrysa.net"
            },
            "to": [
                {"email": to_email}
            ],
            "subject": "Reset Your Password",
            "htmlContent": f"""
                <h2>Password Reset</h2>
                <p>Click below to reset your password:</p>
                <a href="http://localhost:5000/api/auth/reset-password/{token}">
                    Reset Password
                </a>
            """
        }

        return EmailService._send_email(payload)


    # ---------------- DELETE CONFIRMATION ----------------
    @staticmethod
    def send_delete_confirmation_email(to_email, token):

        payload = {
            "sender": {
                "name": "Fountain Ministry SA",
                "email": "no-reply@fountainministrysa.net"
            },
            "to": [
                {"email": to_email}
            ],
            "subject": "Confirm Account Deletion",
            "htmlContent": f"""
                <h2>Account Deletion Request</h2>
                <p>If this was you, confirm deletion below:</p>
                <a href="http://localhost:5000/api/auth/confirm-delete/{token}">
                    Confirm Delete
                </a>
            """
        }

        return EmailService._send_email(payload)