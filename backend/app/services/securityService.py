import bcrypt
from app.utils.logger import logger


class SecurityService:

    # ---------------- HASH PASSWORD ----------------
    @staticmethod
    def hash(password):

        logger.debug("PASSWORD_HASHING attempt")

        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            logger.debug("PASSWORD_HASHING success")

            return hashed

        except Exception as e:
            logger.error(f"PASSWORD_HASHING failed | error={str(e)}")
            raise


    # ---------------- VERIFY PASSWORD ----------------
    @staticmethod
    def verify(password, hashed):

        logger.debug("PASSWORD_VERIFY attempt")

        try:
            result = bcrypt.checkpw(password.encode(), hashed.encode())

            if result:
                logger.debug("PASSWORD_VERIFY success")
            else:
                logger.debug("PASSWORD_VERIFY failed")

            return result

        except Exception as e:
            logger.error(f"PASSWORD_VERIFY error | error={str(e)}")
            return False