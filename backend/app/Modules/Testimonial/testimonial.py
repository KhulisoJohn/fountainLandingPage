# app/Modules/Testimonial/testimonial.py

from datetime import datetime
from app import db


class Testimonial(db.Model):
    __tablename__ = "testimonials"

    id = db.Column(db.Integer, primary_key=True)

    heading = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)

    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # member | visitor | etc

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heading": self.heading,
            "text": self.text,
            "name": self.name,
            "role": self.role,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
        }