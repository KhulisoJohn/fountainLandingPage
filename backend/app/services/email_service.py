import requests
import os

class EmailService:

    @staticmethod
    def send_welcome_email(to_email, name):

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": os.getenv("BREVO_API_KEY"),
            "content-type": "application/json"
        }

        data = {
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

        response = requests.post(url, json=data, headers=headers)

        return response.status_code, response.json()