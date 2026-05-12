from app.models.user import User
from app import db
from app.utils.logger import logger

class UserRepo:

    @staticmethod
    def find_by_email(email):
        logger.debug(f"Searching user by email: {email}")

        user = User.query.filter_by(email=email).first()

        if user:
            logger.debug(f"User found: {email}")
        else:
            logger.debug(f"No user found with email: {email}")

        return user

    @staticmethod
    def find_by_id(user_id):
        logger.debug(f"Searching user by ID: {user_id}")

        user = User.query.get(user_id)

        if not user:
            logger.warning(f"User not found with ID: {user_id}")

        return user

    @staticmethod
    def save(user):
        try:
            logger.info(f"Saving user: {user.email}")

            db.session.add(user)
            db.session.commit()

            logger.info(f"User saved successfully: {user.email}")
            return user

        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to save user {getattr(user, 'email', None)} | Error: {str(e)}")
            raise