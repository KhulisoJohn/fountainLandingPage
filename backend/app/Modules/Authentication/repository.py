from app import db
from app.Modules.User.user import User
from app.Modules.Authentication.pending_user import PendingUser


class AuthRepository:

    # ---------------- USER ----------------
    def get_user_by_email(self, email: str):
        return User.query.filter_by(email=email).first()

    def get_user_by_id(self, user_id: int):
        return User.query.get(user_id)

    def save_user(self, user: User):
        db.session.add(user)
        db.session.commit()

    # ---------------- PENDING USER ----------------
    def get_pending_by_email(self, email: str):
        return PendingUser.query.filter_by(email=email).first()

    def save_pending(self, pending: PendingUser):
        db.session.add(pending)
        db.session.commit()

    def delete_pending(self, pending: PendingUser):
        db.session.delete(pending)
        db.session.commit()

    def delete_pending_by_email(self, email: str):
        PendingUser.query.filter_by(email=email).delete()
        db.session.commit()