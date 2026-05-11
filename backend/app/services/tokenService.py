import uuid
from datetime import datetime, timedelta
from app import db
from app.models.verificationToken import Token

class TokenService:

    @staticmethod
    def create(user_id, type):

        token = str(uuid.uuid4())

        record = Token(
            user_id=user_id,
            token=token,
            type=type,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )

        db.session.add(record)
        db.session.commit()

        return token

    @staticmethod
    def get(token, type):
        return Token.query.filter_by(
            token=token,
            type=type,
            used=False
        ).first()