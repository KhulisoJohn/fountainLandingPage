from app.models.user import User
from app.repositories.userRepository import UserRepo
from app.services.securityService import SecurityService
from app.services.tokenService import TokenService
from app.services.email_service import EmailService
from app.utils.logger import logger
from app import db


class AuthService:

    # ---------------- REGISTER ----------------
    @staticmethod
    def register(data):

        email = data.get("email")

        logger.info(f"REGISTER attempt | email={email}")

        if UserRepo.find_by_email(email):
            logger.warning(f"REGISTER failed | email={email} | reason=User exists")
            return None, "User already exists"

        user = User(
            full_name=data.get("full_name"),
            email=email,
            password=SecurityService.hash(data.get("password")),
            status="pending",
            email_verified=False
        )

        UserRepo.save(user)

        token = TokenService.create(user.id, "verify_email")

        EmailService.send(
            user.email,
            "Verify Account",
            f"http://localhost:5000/api/auth/verify/{token}"
        )

        logger.info(f"REGISTER success | email={email} | user_id={user.id}")

        return user, None


    # ---------------- LOGIN ----------------
    @staticmethod
    def login(email, password):

        logger.info(f"LOGIN attempt | email={email}")

        user = UserRepo.find_by_email(email)

        if not user:
            logger.warning(f"LOGIN failed | email={email} | reason=User not found")
            return None, "User not found"

        if not SecurityService.verify(password, user.password):
            logger.warning(f"LOGIN failed | email={email} | reason=Invalid password")
            return None, "Invalid password"

        if user.status != "active":
            logger.warning(f"LOGIN blocked | email={email} | reason=Account not active")
            return None, "Account not active"

        logger.info(f"LOGIN success | email={email} | user_id={user.id}")

        return user, None


    # ---------------- VERIFY EMAIL ----------------
    @staticmethod
    def verify_email(token):

        logger.info("EMAIL_VERIFY attempt")

        record = TokenService.get(token, "verify_email")

        if not record:
            logger.warning("EMAIL_VERIFY failed | invalid token")
            return False, "Invalid token"

        user = UserRepo.find_by_id(record.user_id)

        if not user:
            logger.error(f"EMAIL_VERIFY failed | user not found | user_id={record.user_id}")
            return False, "User not found"

        user.status = "active"
        user.email_verified = True
        record.used = True

        db.session.commit()

        logger.info(f"EMAIL_VERIFY success | user_id={user.id}")

        return True, None


    # ---------------- FORGOT PASSWORD ----------------
    @staticmethod
    def forgot_password(email):

        logger.info(f"FORGOT_PASSWORD request | email={email}")

        user = UserRepo.find_by_email(email)

        if not user:
            logger.warning(f"FORGOT_PASSWORD unknown email | email={email}")
            return

        token = TokenService.create(user.id, "reset_password")

        EmailService.send(
            user.email,
            "Reset Password",
            f"http://localhost:5000/api/auth/reset-password/{token}"
        )

        logger.info(f"FORGOT_PASSWORD email sent | email={email}")


    # ---------------- RESET PASSWORD ----------------
    @staticmethod
    def reset_password(token, new_password):

        logger.info("RESET_PASSWORD attempt")

        record = TokenService.get(token, "reset_password")

        if not record:
            logger.warning("RESET_PASSWORD failed | invalid token")
            return False, "Invalid token"

        user = UserRepo.find_by_id(record.user_id)

        if not user:
            logger.error(f"RESET_PASSWORD failed | user not found | user_id={record.user_id}")
            return False, "User not found"

        user.password = SecurityService.hash(new_password)
        record.used = True

        db.session.commit()

        logger.info(f"RESET_PASSWORD success | user_id={user.id}")

        return True, None


    # ---------------- CHANGE PASSWORD ----------------
    @staticmethod
    def change_password(user_id, old_password, new_password):

        logger.info(f"CHANGE_PASSWORD attempt | user_id={user_id}")

        user = UserRepo.find_by_id(user_id)

        if not user:
            logger.warning(f"CHANGE_PASSWORD failed | user not found | user_id={user_id}")
            return False, "User not found"

        if not SecurityService.verify(old_password, user.password):
            logger.warning(f"CHANGE_PASSWORD failed | wrong password | user_id={user_id}")
            return False, "Wrong password"

        user.password = SecurityService.hash(new_password)
        db.session.commit()

        logger.info(f"CHANGE_PASSWORD success | user_id={user_id}")

        return True, None


    # ---------------- DELETE ACCOUNT REQUEST ----------------
    @staticmethod
    def request_delete_account(user_id):

        logger.warning(f"DELETE_ACCOUNT request | user_id={user_id}")

        user = UserRepo.find_by_id(user_id)

        token = TokenService.create(user_id, "delete_account")

        EmailService.send(
            user.email,
            "Confirm Account Deletion",
            f"http://localhost:5000/api/auth/confirm-delete/{token}"
        )

        logger.info(f"DELETE_ACCOUNT email sent | user_id={user_id}")

        return True


    # ---------------- CONFIRM DELETE ----------------
    @staticmethod
    def confirm_delete(token):

        logger.warning("CONFIRM_DELETE attempt")

        record = TokenService.get(token, "delete_account")

        if not record:
            logger.warning("CONFIRM_DELETE failed | invalid token")
            return False, "Invalid token"

        user = UserRepo.find_by_id(record.user_id)

        if not user:
            logger.error(f"CONFIRM_DELETE failed | user not found | user_id={record.user_id}")
            return False, "User not found"

        user.is_active = False
        user.status = "deleted"
        record.used = True

        db.session.commit()

        logger.warning(f"ACCOUNT DELETED | user_id={user.id}")

        return True, None