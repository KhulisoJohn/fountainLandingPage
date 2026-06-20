# app/Modules/Testimonial/service.py

from app import db
from app.Modules.Testimonial.testimonial import Testimonial
from app.Modules.User.user import User


class TestimonialService:

    ALLOWED_ROLES = ["member", "visitor", "guest", "admin"]

    def create_testimonial(self, user_id, data):

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        heading = (data.get("heading") or "").strip()
        text = (data.get("text") or "").strip()
        name = (data.get("name") or "").strip()
        role = (data.get("role") or "").strip().lower()

        if not heading or not text or not name or not role:
            return {"error": "All fields are required"}, 400

        if role not in self.ALLOWED_ROLES:
            return {"error": "Invalid role selected"}, 400

        testimonial = Testimonial(
            heading=heading,
            text=text,
            name=name,
            role=role,
            user_id=user_id
        )

        db.session.add(testimonial)
        db.session.commit()

        return {
            "message": "Testimonial created successfully",
            "testimonial": testimonial.to_dict()
        }, 201

    def get_all_testimonials(self):

        testimonials = Testimonial.query.order_by(
            Testimonial.created_at.desc()
        ).all()

        return {
            "testimonials": [t.to_dict() for t in testimonials]
        }, 200