from datetime import datetime

from app import db


class PendingUser(db.Model):
    __tablename__ = "pending_users"

    # ---------------- CORE ----------------
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # ---------------- VERIFICATION FLOW ----------------
    verification_token = db.Column(db.String(500), nullable=True)
    token_expires_at = db.Column(db.DateTime, nullable=True)
    attempts = db.Column(db.Integer, default=0, nullable=False)

    # ---------------- AUDIT ----------------
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ---------------- STATUS ----------------
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_expired = db.Column(db.Boolean, default=False, nullable=False)

    # ---------------- SECURITY HELPERS ----------------
    def mark_verified(self):
        self.is_verified = True

    def expire(self):
        self.is_expired = True

    def increment_attempts(self):
        self.attempts += 1

    def is_token_valid(self):
        if not self.token_expires_at:
            return False
        return datetime.utcnow() < self.token_expires_at

    # ---------------- SERIALIZATION ----------------
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }