from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.services.auth_service import AuthService
from app.utils.logger import logger

auth_bp = Blueprint("auth", __name__)


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()
    email = data.get("email")

    logger.info(f"REGISTER request | email={email}")

    _, err = AuthService.register(data)

    if err:
        logger.warning(f"REGISTER failed | email={email} | reason={err}")
        return {"error": err}, 400

    logger.info(f"REGISTER success | email={email}")
    return {"message": "Check email"}, 201


# ---------------- VERIFY EMAIL ----------------
@auth_bp.route("/verify/<token>")
def verify(token):

    logger.info("EMAIL_VERIFY request")

    success, err = AuthService.verify_email(token)

    if not success:
        logger.warning(f"EMAIL_VERIFY failed | reason={err}")
        return {"error": err}, 400

    logger.info("EMAIL_VERIFY success")
    return {"message": "Verified"}, 200


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    email = data.get("email")

    logger.info(f"LOGIN request | email={email}")

    user, err = AuthService.login(email, data["password"])

    if err:
        logger.warning(f"LOGIN failed | email={email} | reason={err}")
        return {"error": err}, 401

    token = create_access_token(identity={
        "id": user.id,
        "role": user.role
    })

    logger.info(f"LOGIN success | user_id={user.id}")

    return {"token": token}, 200


# ---------------- FORGOT PASSWORD ----------------
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()
    email = data.get("email")

    logger.info(f"FORGOT_PASSWORD request | email={email}")

    AuthService.forgot_password(email)

    return {"message": "If account exists, reset email sent"}, 200


# ---------------- RESET PASSWORD ----------------
@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):

    data = request.get_json()

    logger.info("RESET_PASSWORD request")

    success, err = AuthService.reset_password(token, data["new_password"])

    if not success:
        logger.warning(f"RESET_PASSWORD failed | reason={err}")
        return {"error": err}, 400

    logger.info("RESET_PASSWORD success")

    return {"message": "Password updated"}, 200


# ---------------- CHANGE PASSWORD ----------------
@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():

    user_id = get_jwt_identity()["id"]
    data = request.get_json()

    logger.info(f"CHANGE_PASSWORD request | user_id={user_id}")

    success, err = AuthService.change_password(
        user_id,
        data["old_password"],
        data["new_password"]
    )

    if not success:
        logger.warning(f"CHANGE_PASSWORD failed | user_id={user_id} | reason={err}")
        return {"error": err}, 401

    logger.info(f"CHANGE_PASSWORD success | user_id={user_id}")

    return {"message": "Password changed"}, 200


# ---------------- DELETE ACCOUNT ----------------
@auth_bp.route("/delete-account", methods=["POST"])
@jwt_required()
def delete_account_request():

    user_id = get_jwt_identity()["id"]

    logger.warning(f"DELETE_ACCOUNT request | user_id={user_id}")

    AuthService.request_delete_account(user_id)

    return {"message": "Check email to confirm deletion"}, 200


# ---------------- CONFIRM DELETE ----------------
@auth_bp.route("/confirm-delete/<token>", methods=["GET"])
def confirm_delete(token):

    logger.warning("CONFIRM_DELETE request")

    success, err = AuthService.confirm_delete(token)

    if not success:
        logger.warning(f"CONFIRM_DELETE failed | reason={err}")
        return {"error": err}, 400

    logger.warning("ACCOUNT DELETED")

    return {"message": "Account deleted"}, 200


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    user_id = get_jwt_identity()["id"]

    logger.info(f"LOGOUT request | user_id={user_id}")

    return {"message": "Logout successful (client clears token)"}, 200