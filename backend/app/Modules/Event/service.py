from datetime import datetime
from app import db
from app.Modules.Event.event import Event


class EventService:

    @staticmethod
    def list_events():
        return Event.query.order_by(Event.event_date.asc()).all()

    @staticmethod
    def get_event(event_id: int):
        return Event.query.get(event_id)

    @staticmethod
    def create_event(data: dict):
        title = (data.get("title") or "").strip()
        event_date_raw = data.get("event_date")

        if not title or not event_date_raw:
            return None, "MISSING_FIELDS"

        try:
            event_date = datetime.fromisoformat(event_date_raw)
        except Exception:
            return None, "INVALID_DATE"

        event = Event(
            title=title,
            description=data.get("description"),
            location=data.get("location"),
            event_date=event_date,
            image_url=data.get("image_url"),
        )

        db.session.add(event)
        db.session.commit()

        return event, None

    @staticmethod
    def update_event(event_id: int, data: dict):
        event = Event.query.get(event_id)
        if not event:
            return None, "NOT_FOUND"

        if "title" in data:
            event.title = data["title"]

        if "description" in data:
            event.description = data["description"]

        if "location" in data:
            event.location = data["location"]

        if "image_url" in data:
            event.image_url = data["image_url"]

        if "event_date" in data:
            try:
                event.event_date = datetime.fromisoformat(data["event_date"])
            except Exception:
                return None, "INVALID_DATE"

        db.session.commit()
        return event, None

    @staticmethod
    def delete_event(event_id: int):
        event = Event.query.get(event_id)
        if not event:
            return False

        db.session.delete(event)
        db.session.commit()
        return True