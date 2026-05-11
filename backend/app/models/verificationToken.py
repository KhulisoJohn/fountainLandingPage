from app import db
from datetime import datetime

class Token(db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    token = db.Column(db.String(255), unique=True, nullable=False)

    type = db.Column(db.String(50))
    # verify_email | reset_password | delete_account

    used = db.Column(db.Boolean, default=False)

    expires_at = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)