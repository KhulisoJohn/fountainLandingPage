from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.utils.decorators import admin_required
from app.Modules.Event.service import EventService


event_bp = Blueprint("event_bp", __name__)


# ---------------- LIST ----------------
@event_bp.route("", methods=["GET"])
@jwt_required()
def list_events():
    events = EventService.list_events()
    return jsonify({"events": [e.to_dict() for e in events]}), 200


# ---------------- GET ONE ----------------
@event_bp.route("/<int:event_id>", methods=["GET"])
@jwt_required()
def get_event(event_id):
    event = EventService.get_event(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    return jsonify({"event": event.to_dict()}), 200


# ---------------- CREATE ----------------
@event_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
def create_event():
    data = request.get_json() or {}

    event, error = EventService.create_event(data)

    if error == "MISSING_FIELDS":
        return jsonify({"error": "Title and event_date are required"}), 400

    if error == "INVALID_DATE":
        return jsonify({"error": "event_date must be ISO 8601 format"}), 400

    return jsonify({
        "message": "Event created",
        "event": event.to_dict()
    }), 201


# ---------------- UPDATE ----------------
@event_bp.route("/<int:event_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_event(event_id):
    data = request.get_json() or {}

    event, error = EventService.update_event(event_id, data)

    if error == "NOT_FOUND":
        return jsonify({"error": "Event not found"}), 404

    if error == "INVALID_DATE":
        return jsonify({"error": "event_date must be ISO 8601 format"}), 400

    return jsonify({
        "message": "Event updated",
        "event": event.to_dict()
    }), 200


# ---------------- DELETE ----------------
@event_bp.route("/<int:event_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_event(event_id):
    success = EventService.delete_event(event_id)

    if not success:
        return jsonify({"error": "Event not found"}), 404

    return jsonify({"message": "Event deleted"}), 200