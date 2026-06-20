from datetime import datetime
from app import db
from app.Modules.User.user import User


class UserService:

    @staticmethod
    def get_user_by_id(user_id: int):
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id: int, data: dict):
        user = User.query.get(user_id)
        if not user:
            return None

        # Only allow safe fields to update
        if "name" in data:
            user.name = data["name"].strip()

        if "email" in data:
            user.email = data["email"].strip().lower()

        # POPIA / consent fields
        if "popia_consent" in data:
            user.popia_consent = bool(data["popia_consent"])
            user.popia_consent_at = datetime.utcnow()

        if "terms_accepted" in data:
            user.terms_accepted = bool(data["terms_accepted"])
            user.terms_accepted_at = datetime.utcnow()

        if "marketing_consent" in data:
            user.marketing_consent = bool(data["marketing_consent"])

        if "is_active" in data:
            user.is_active = bool(data["is_active"])

        user.updated_at = datetime.utcnow()

        db.session.commit()
        return user