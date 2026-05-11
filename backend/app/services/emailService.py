import requests
import os

class EmailService:

    @staticmethod
    def send(to, subject, html):

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "api-key": os.getenv("BREVO_API_KEY"),
            "content-type": "application/json"
        }

        data = {
            "sender": {"name": "Fountain Ministry", "email": "no-reply@fountain.com"},
            "to": [{"email": to}],
            "subject": subject,
            "htmlContent": html
        }

        requests.post(url, json=data, headers=headers)