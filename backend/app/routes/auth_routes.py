from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.services.auth_service import AuthService
from app.services.tokenService import TokenService
from app.services.securityService import SecurityService
from app.services.email_service import EmailService
from app.repositories.userRepository import UserRepo
from app import db
from app.models.verificationToken import Token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():

    user, err = AuthService.register(request.get_json())

    if err:
        return {"error": err}, 400

    return {"message": "Check email"}, 201

@auth_bp.route("/verify/<token>")
def verify(token):

    record = TokenService.get(token, "verify_email")

    if not record:
        return {"error": "Invalid token"}, 400

    user = UserRepo.find_by_id(record.user_id)

    user.status = "active"
    user.email_verified = True

    record.used = True

    db.session.commit()

    return {"message": "Verified"}, 200

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = AuthService.login(data["email"], data["password"])

    if not user:
        return {"error": "Invalid or unverified"}, 401

    token = create_access_token(identity={
        "id": user.id,
        "role": user.role
    })

    return {"token": token}, 200

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()
    email = data["email"]

    user = UserRepo.find_by_email(email)

    # Always return same response (security best practice)
    if user:
        token = TokenService.create(user.id, "reset_password")

        EmailService.send(
            user.email,
            "Reset Password",
            f"http://localhost:5000/api/auth/reset-password/{token}"
        )

    return {"message": "If account exists, reset email sent"}, 200

@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):

    record = TokenService.get(token, "reset_password")

    if not record:
        return {"error": "Invalid token"}, 400

    data = request.get_json()

    user = UserRepo.find_by_id(record.user_id)

    user.password = SecurityService.hash(data["new_password"])

    record.used = True

    db.session.commit()

    return {"message": "Password updated"}, 200

from flask_jwt_extended import jwt_required, get_jwt_identity

@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():

    user_id = get_jwt_identity()["id"]
    user = UserRepo.find_by_id(user_id)

    data = request.get_json()

    if not SecurityService.verify(data["old_password"], user.password):
        return {"error": "Wrong password"}, 401

    user.password = SecurityService.hash(data["new_password"])

    db.session.commit()

    return {"message": "Password changed"}, 200

@auth_bp.route("/delete-account", methods=["POST"])
@jwt_required()
def delete_account_request():

    user_id = get_jwt_identity()["id"]

    token = TokenService.create(user_id, "delete_account")

    user = UserRepo.find_by_id(user_id)

    EmailService.send(
        user.email,
        "Confirm Account Deletion",
        f"http://localhost:5000/api/auth/confirm-delete/{token}"
    )

    return {"message": "Check email to confirm deletion"}, 200

@auth_bp.route("/confirm-delete/<token>", methods=["GET"])
def confirm_delete(token):

    record = TokenService.get(token, "delete_account")

    if not record:
        return {"error": "Invalid token"}, 400

    user = UserRepo.find_by_id(record.user_id)

    user.is_active = False
    user.status = "deleted"

    record.used = True

    db.session.commit()

    return {"message": "Account deleted"}, 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    return {"message": "Logout successful (client clears token)"}, 200