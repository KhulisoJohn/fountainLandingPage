import uuid
from datetime import datetime, timedelta

from app import db
from app.models.verificationToken import Token
from app.utils.logger import logger


class TokenService:

    # ---------------- CREATE TOKEN ----------------
    @staticmethod
    def create(user_id, token_type):

        logger.info(f"TOKEN_CREATE | user_id={user_id} | type={token_type}")

        try:
            token = str(uuid.uuid4())

            record = Token(
                user_id=user_id,
                token=token,
                type=token_type,
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )

            db.session.add(record)
            db.session.commit()

            logger.info(f"TOKEN_CREATE success | user_id={user_id} | type={token_type}")

            return token

        except Exception as e:
            db.session.rollback()
            logger.error(f"TOKEN_CREATE failed | user_id={user_id} | error={str(e)}")
            raise


    # ---------------- GET TOKEN ----------------
    @staticmethod
    def get(token, token_type):

        logger.info(f"TOKEN_VALIDATE attempt | type={token_type}")

        try:
            record = Token.query.filter_by(
                token=token,
                type=token_type,
                used=False
            ).first()

            if not record:
                logger.warning(f"TOKEN_VALIDATE failed | type={token_type}")
                return None

            # Optional: expiry check
            if record.expires_at and record.expires_at < datetime.utcnow():
                logger.warning(f"TOKEN_EXPIRED | type={token_type} | user_id={record.user_id}")
                return None

            logger.info(f"TOKEN_VALIDATE success | type={token_type} | user_id={record.user_id}")

            return record

        except Exception as e:
            logger.error(f"TOKEN_VALIDATE error | type={token_type} | error={str(e)}")
            return None