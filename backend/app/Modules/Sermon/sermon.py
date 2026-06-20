from datetime import datetime

from app import db


class Sermon(db.Model):
    __tablename__ = "sermons"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    speaker = db.Column(db.String(120))
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    sermon_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "speaker": self.speaker,
            "description": self.description,
            "video_url": self.video_url,
            "sermon_date": self.sermon_date.isoformat(),
        }
