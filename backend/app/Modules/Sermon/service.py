from datetime import datetime
from app import db
from app.Modules.Sermon.sermon import Sermon


class SermonService:

    @staticmethod
    def list_sermons():
        return Sermon.query.order_by(Sermon.sermon_date.desc()).all()

    @staticmethod
    def get_sermon(sermon_id: int):
        return Sermon.query.get(sermon_id)

    @staticmethod
    def create_sermon(data: dict):
        try:
            sermon_date = datetime.fromisoformat(data.get("sermon_date"))
        except Exception:
            return None, "INVALID_DATE"

        sermon = Sermon(
            title=data.get("title").strip(),
            speaker=data.get("speaker"),
            description=data.get("description"),
            video_url=data.get("video_url"),
            sermon_date=sermon_date,
        )

        db.session.add(sermon)
        db.session.commit()

        return sermon, None

    @staticmethod
    def update_sermon(sermon_id: int, data: dict):
        sermon = Sermon.query.get(sermon_id)
        if not sermon:
            return None, "NOT_FOUND"

        if "title" in data:
            sermon.title = data["title"]

        if "speaker" in data:
            sermon.speaker = data["speaker"]

        if "description" in data:
            sermon.description = data["description"]

        if "video_url" in data:
            sermon.video_url = data["video_url"]

        if "sermon_date" in data:
            try:
                sermon.sermon_date = datetime.fromisoformat(data["sermon_date"])
            except Exception:
                return None, "INVALID_DATE"

        db.session.commit()
        return sermon, None

    @staticmethod
    def delete_sermon(sermon_id: int):
        sermon = Sermon.query.get(sermon_id)
        if not sermon:
            return False

        db.session.delete(sermon)
        db.session.commit()
        return True