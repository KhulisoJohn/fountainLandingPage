from app import db
from app.Modules.Prayer.prayer import Prayer


class PrayerService:

    @staticmethod
    def create_prayer(user_id: int, request_text: str):
        prayer = Prayer(user_id=user_id, request_text=request_text)
        db.session.add(prayer)
        db.session.commit()
        return prayer

    @staticmethod
    def get_user_prayers(user_id: int):
        return Prayer.query.filter_by(user_id=user_id)\
            .order_by(Prayer.created_at.desc()).all()

    @staticmethod
    def get_all_prayers():
        return Prayer.query.order_by(Prayer.created_at.desc()).all()

    @staticmethod
    def update_status(prayer_id: int, status: str):
        prayer = Prayer.query.get(prayer_id)
        if not prayer:
            return None

        prayer.status = status
        db.session.commit()
        return prayer