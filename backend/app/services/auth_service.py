from app.models.user import User
from app.repositories.userRepository import UserRepo
from app.services.securityService import SecurityService
from app.services.tokenService import TokenService
from app.services.email_service import EmailService

class AuthService:

    @staticmethod
    def register(data):

        if UserRepo.find_by_email(data["email"]):
            return None, "User exists"

        user = User(
            full_name=data["full_name"],
            email=data["email"],
            password=SecurityService.hash(data["password"]),
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

        return user, None

    @staticmethod
    def login(email, password):

        user = UserRepo.find_by_email(email)

        if not user:
            return None

        if not SecurityService.verify(password, user.password):
            return None

        if user.status != "active":
            return None

        return user