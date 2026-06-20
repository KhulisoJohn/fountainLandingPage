from datetime import datetime

from app import db


class Prayer(db.Model):
    __tablename__ = "prayers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    request_text = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False)  # pending / answered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "request_text": self.request_text,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
