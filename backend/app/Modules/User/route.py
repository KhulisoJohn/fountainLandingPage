from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.Modules.User.service import UserService

user_bp = Blueprint("user_bp", __name__, url_prefix="/api/user")


# ---------------- GET USER ----------------
@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = int(get_jwt_identity())

    user = UserService.get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_dict()}), 200


# ---------------- UPDATE USER ----------------
@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    user = UserService.update_user(user_id, data)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": "User updated successfully",
        "user": user.to_dict()
    }), 200