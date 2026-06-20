from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.decorators import admin_required
from app.Modules.Prayer.service import PrayerService

prayer_bp = Blueprint("prayer_bp", __name__)


@prayer_bp.route("", methods=["POST"])
@jwt_required()
def create_prayer():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    request_text = (data.get("request_text") or "").strip()

    if not request_text:
        return jsonify({"error": "Prayer request text is required"}), 400

    prayer = PrayerService.create_prayer(user_id, request_text)

    return jsonify({
        "message": "Your prayer request has been submitted.",
        "prayer": prayer.to_dict(),
    }), 201


@prayer_bp.route("/mine", methods=["GET"])
@jwt_required()
def my_prayers():
    user_id = int(get_jwt_identity())
    prayers = PrayerService.get_user_prayers(user_id)

    return jsonify({
        "prayers": [p.to_dict() for p in prayers]
    }), 200


@prayer_bp.route("/admin", methods=["GET"])
@jwt_required()
@admin_required
def list_all_prayers():
    prayers = PrayerService.get_all_prayers()

    return jsonify({
        "prayers": [p.to_dict() for p in prayers]
    }), 200


@prayer_bp.route("/admin/<int:prayer_id>/status", methods=["PUT"])
@jwt_required()
@admin_required
def update_prayer_status(prayer_id):
    data = request.get_json() or {}
    status = data.get("status")

    if status not in ("pending", "answered"):
        return jsonify({"error": "Status must be 'pending' or 'answered'"}), 400

    prayer = PrayerService.update_status(prayer_id, status)

    if not prayer:
        return jsonify({"error": "Prayer request not found"}), 404

    return jsonify({
        "message": "Status updated",
        "prayer": prayer.to_dict()
    }), 200