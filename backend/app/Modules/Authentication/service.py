from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from flask import current_app

from app.Modules.Authentication.repository import AuthRepository
from app.Modules.Authentication.pending_user import PendingUser
from app.Modules.User.user import User

from app.utils.tokens import generate_token, verify_token
from app.utils.jwt_blacklist import is_token_revoked, blacklist_token
from app.utils.email_service import (
    send_verification_email,
    send_password_reset_email,
)

EMAIL_VERIFY_SALT = "email-verify"
PASSWORD_RESET_SALT = "password-reset"


class AuthService:

    def __init__(self):
        self.repo = AuthRepository()

    # ---------------- REGISTER ----------------
    def register(self, dto):

        if self.repo.get_user_by_email(dto.email):
            return {"error": "Email already exists"}, 409

        existing = self.repo.get_pending_by_email(dto.email)
        if existing:
            self.repo.delete_pending(existing)

        pending = PendingUser(
            name=dto.name,
            email=dto.email,
            password_hash=generate_password_hash(dto.password),
        )

        self.repo.save_pending(pending)

        token = generate_token(dto.email, EMAIL_VERIFY_SALT)
        send_verification_email(dto.email, dto.name, token)

        return {"message": "Check email to verify account"}, 201

    # ---------------- VERIFY EMAIL ----------------
    def verify_email(self, token):

        email = verify_token(
            token,
            EMAIL_VERIFY_SALT,
            current_app.config["EMAIL_VERIFICATION_MAX_AGE"]
        )

        if not email:
            return {"error": "Invalid or expired token"}, 400

        if self.repo.get_user_by_email(email):
            self.repo.delete_pending_by_email(email)
            return {"message": "Already verified"}, 200

        pending = self.repo.get_pending_by_email(email)
        if not pending:
            return {"error": "No pending account"}, 404

        user = User(
            name=pending.name,
            email=pending.email,
            password_hash=pending.password_hash,
            role="member",
            is_verified=True,
            is_active=True,
            popia_consent=True,
            terms_accepted=True,
            marketing_consent=False,
        )

        self.repo.save_user(user)
        self.repo.delete_pending(pending)

        return {"message": "Email verified"}, 200

    # ---------------- LOGIN ----------------
    def login(self, dto):

        user = self.repo.get_user_by_email(dto.email)

        if not user or not user.check_password(dto.password):
            return {"error": "Invalid credentials"}, 401

        if not user.is_verified:
            return {"error": "Verify email first"}, 403

        token = create_access_token(identity=user.id)

        return {
            "access_token": token,
            "user": user.to_dict()
        }, 200

    # ---------------- VALIDATE TOKEN ----------------
    def validate_token(self, jwt_payload):

        jti = jwt_payload.get("jti")

        if is_token_revoked(jti):
            return {"valid": False, "error": "Token revoked"}, 401

        user_id = jwt_payload.get("sub")

        user = self.repo.get_user_by_id(int(user_id))

        if not user:
            return {"valid": False, "error": "User not found"}, 404

        if not user.is_active or user.is_deleted:
            return {"valid": False, "error": "Account inactive"}, 403

        return {
            "valid": True,
            "user": user.to_dict()
        }, 200

    # ---------------- FORGOT PASSWORD ----------------
    def forgot_password(self, dto):

        user = self.repo.get_user_by_email(dto.email)

        if user:
            token = generate_token(dto.email, PASSWORD_RESET_SALT)
            send_password_reset_email(dto.email, user.name, token)

        return {"message": "If account exists, email sent"}, 200

    # ---------------- RESET PASSWORD ----------------
    def reset_password(self, dto):

        email = verify_token(
            dto.token,
            PASSWORD_RESET_SALT,
            current_app.config["PASSWORD_RESET_MAX_AGE"]
        )

        if not email:
            return {"error": "Invalid token"}, 400

        user = self.repo.get_user_by_email(email)

        if not user:
            return {"error": "User not found"}, 404

        user.set_password(dto.password)
        self.repo.save_user(user)

        return {"message": "Password updated"}, 200

    # ---------------- ME ----------------
    def get_me(self, user_id):

        user = self.repo.get_user_by_id(user_id)

        if not user:
            return {"error": "Not found"}, 404

        return {"user": user.to_dict()}, 200

    # ---------------- LOGOUT ----------------
    def logout(self, jti: str):

        blacklist_token(jti)

        return {"message": "Logged out successfully"}, 200