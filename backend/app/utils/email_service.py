import requests
from flask import current_app
from app.utils.logger import logger

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_email(to_email: str, to_name: str, subject: str, html_content: str) -> bool:
    api_key = current_app.config["BREVO_API_KEY"]
    sender_email = current_app.config["BREVO_SENDER_EMAIL"]
    sender_name = current_app.config["BREVO_SENDER_NAME"]

    logger.info(f"BREVO_KEY_USED = {api_key}")

    if not api_key:
        logger.error("BREVO_API_KEY is missing or None")
        return False

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": sender_name,
            "email": sender_email
        },
        "to": [
            {
                "email": to_email,
                "name": to_name
            }
        ],
        "subject": subject,
        "htmlContent": html_content,
    }

    try:
        response = requests.post(
            BREVO_API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        # IMPORTANT: log full Brevo response before failing
        if response.status_code >= 400:
            logger.error("BREVO_REQUEST_FAILED")
            logger.error(f"STATUS_CODE = {response.status_code}")
            logger.error(f"RESPONSE_BODY = {response.text}")
            return False

        logger.info(f"EMAIL_SENT | to={to_email} | subject={subject}")
        return True

    except requests.RequestException as e:
        logger.error("EMAIL_SEND_EXCEPTION")
        logger.error(f"ERROR = {str(e)}")
        return False


def send_verification_email(to_email: str, to_name: str, token: str) -> bool:
    link = f"{current_app.config['FRONTEND_URL']}/verify-email.html?token={token}"

    html = f"""
        <h2>Welcome to Fountain of Fire Ministry</h2>
        <p>Hi {to_name},</p>
        <p>Please verify your email address to activate your account.</p>
        <p><a href="{link}">Verify my account</a></p>
        <p>This link expires in 24 hours.</p>
    """

    return send_email(
        to_email,
        to_name,
        "Verify your Fountain account",
        html
    )


def send_password_reset_email(to_email: str, to_name: str, token: str) -> bool:
    link = f"{current_app.config['FRONTEND_URL']}/reset-password.html?token={token}"

    html = f"""
        <h2>Password Reset Request</h2>
        <p>Hi {to_name},</p>
        <p>Click below to reset your password:</p>
        <p><a href="{link}">Reset Password</a></p>
        <p>This link expires in 1 hour.</p>
    """

    return send_email(
        to_email,
        to_name,
        "Reset your Fountain account password",
        html
    )


def send_account_deletion_email(to_email: str, to_name: str, token: str) -> bool:
    link = f"{current_app.config['FRONTEND_URL']}/confirm-delete.html?token={token}"

    html = f"""
        <h2>Confirm Account Deletion</h2>
        <p>Hi {to_name},</p>
        <p>This action is permanent and cannot be undone.</p>
        <p><a href="{link}">Confirm deletion</a></p>
        <p>This link expires in 1 hour.</p>
    """

    return send_email(
        to_email,
        to_name,
        "Confirm deletion of your Fountain account",
        html
    )