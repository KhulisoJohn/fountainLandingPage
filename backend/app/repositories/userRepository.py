from app.models.user import User
from app import db

class UserRepo:

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_id(id):
        return User.query.get(id)

    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()
        return user