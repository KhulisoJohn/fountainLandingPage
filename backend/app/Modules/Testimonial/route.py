# app/Modules/Testimonial/route.py

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.Modules.Testimonial.service import TestimonialService

testimonial_bp = Blueprint("testimonial_bp", __name__, url_prefix="/api/testimonials")

service = TestimonialService()


# ---------------- CREATE TESTIMONIAL ----------------
@testimonial_bp.route("", methods=["POST"])
@jwt_required()
def create_testimonial():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    return service.create_testimonial(user_id, data)


# ---------------- GET ALL TESTIMONIALS ----------------
@testimonial_bp.route("", methods=["GET"])
def get_testimonials():
    return service.get_all_testimonials()