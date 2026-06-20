from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.utils.decorators import admin_required
from app.Modules.Sermon.service import SermonService


sermon_bp = Blueprint("sermon_bp", __name__)


# ---------------- LIST ----------------
@sermon_bp.route("", methods=["GET"])
@jwt_required()
def list_sermons():
    sermons = SermonService.list_sermons()
    return jsonify({"sermons": [s.to_dict() for s in sermons]}), 200


# ---------------- GET ONE ----------------
@sermon_bp.route("/<int:sermon_id>", methods=["GET"])
@jwt_required()
def get_sermon(sermon_id):
    sermon = SermonService.get_sermon(sermon_id)

    if not sermon:
        return jsonify({"error": "Sermon not found"}), 404

    return jsonify({"sermon": sermon.to_dict()}), 200


# ---------------- CREATE ----------------
@sermon_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
def create_sermon():
    data = request.get_json() or {}

    if not data.get("title") or not data.get("sermon_date"):
        return jsonify({"error": "Title and sermon_date are required"}), 400

    sermon, error = SermonService.create_sermon(data)

    if error == "INVALID_DATE":
        return jsonify({"error": "sermon_date must be ISO 8601 format"}), 400

    return jsonify({
        "message": "Sermon created",
        "sermon": sermon.to_dict()
    }), 201


# ---------------- UPDATE ----------------
@sermon_bp.route("/<int:sermon_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_sermon(sermon_id):
    data = request.get_json() or {}

    sermon, error = SermonService.update_sermon(sermon_id, data)

    if error == "NOT_FOUND":
        return jsonify({"error": "Sermon not found"}), 404

    if error == "INVALID_DATE":
        return jsonify({"error": "sermon_date must be ISO 8601 format"}), 400

    return jsonify({
        "message": "Sermon updated",
        "sermon": sermon.to_dict()
    }), 200


# ---------------- DELETE ----------------
@sermon_bp.route("/<int:sermon_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_sermon(sermon_id):
    success = SermonService.delete_sermon(sermon_id)

    if not success:
        return jsonify({"error": "Sermon not found"}), 404

    return jsonify({"message": "Sermon deleted"}), 200