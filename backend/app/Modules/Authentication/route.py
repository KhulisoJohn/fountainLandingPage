from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.Modules.Authentication.service import AuthService
from app.Modules.Authentication.dto import (
    RegisterDTO,
    LoginDTO,
    VerifyEmailDTO,
    ForgotPasswordDTO,
    ResetPasswordDTO
)

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

service = AuthService()


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    try:
        dto = RegisterDTO(**data)
    except Exception:
        return {"error": "Invalid request payload"}, 400

    return service.register(dto)


# ---------------- VERIFY EMAIL ----------------
@auth_bp.route("/verify-email", methods=["POST"])
def verify_email():
    data = request.get_json() or {}
    try:
        dto = VerifyEmailDTO(**data)
    except Exception:
        return {"error": "Invalid request payload"}, 400

    return service.verify_email(dto.token)


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    try:
        dto = LoginDTO(**data)
    except Exception:
        return {"error": "Invalid request payload"}, 400

    return service.login(dto)


# ---------------- FORGOT PASSWORD ----------------
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}
    try:
        dto = ForgotPasswordDTO(**data)
    except Exception:
        return {"error": "Invalid request payload"}, 400

    return service.forgot_password(dto)


# ---------------- RESET PASSWORD ----------------
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}
    try:
        dto = ResetPasswordDTO(**data)
    except Exception:
        return {"error": "Invalid request payload"}, 400

    return service.reset_password(dto)


# ---------------- ME ----------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    return service.get_me(user_id)


# ---------------- VALIDATE ----------------
@auth_bp.route("/validate", methods=["GET"])
@jwt_required()
def validate():
    jwt_payload = get_jwt()
    return service.validate_token(jwt_payload)


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    return service.logout(jti)