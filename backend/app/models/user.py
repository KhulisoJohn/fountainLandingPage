from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(50), default="member")
    status = db.Column(db.String(20), default="pending")  # pending | active

    # POPIA COMPLIANCE FIELDS
    accepted_terms = db.Column(db.Boolean, default=False, nullable=False)

    accepted_privacy_policy = db.Column(db.Boolean, default=False, nullable=False)

    consent_timestamp = db.Column(db.DateTime, nullable=True)

    consent_ip_address = db.Column(db.String(45), nullable=True)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"