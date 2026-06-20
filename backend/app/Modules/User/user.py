from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = "users"

    # ---------------- CORE ----------------
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="member", nullable=False)  # member | admin

    # ---------------- AUDIT / TRACKING ----------------
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)

    # ---------------- POPIA / CONSENT ----------------
    popia_consent = db.Column(db.Boolean, default=False, nullable=False)
    popia_consent_at = db.Column(db.DateTime, nullable=True)

    terms_accepted = db.Column(db.Boolean, default=False, nullable=False)
    terms_accepted_at = db.Column(db.DateTime, nullable=True)

    marketing_consent = db.Column(db.Boolean, default=False, nullable=False)

    # ---------------- ACCOUNT STATUS ----------------
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    # ---------------- RELATIONSHIPS ----------------
    prayers = db.relationship(
        "Prayer",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ---------------- SECURITY METHODS ----------------
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # ---------------- LIFECYCLE HELPERS ----------------
    def mark_verified(self):
        self.is_verified = True

    def mark_deleted(self):
        self.is_deleted = True
        self.is_active = False

    def mark_login(self):
        self.last_login_at = datetime.utcnow()

    def accept_terms(self):
        self.terms_accepted = True
        self.terms_accepted_at = datetime.utcnow()

    def accept_popia(self):
        self.popia_consent = True
        self.popia_consent_at = datetime.utcnow()

    # ---------------- SERIALIZATION ----------------
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }