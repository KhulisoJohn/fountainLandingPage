import bcrypt

class SecurityService:

    @staticmethod
    def hash(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify(password, hashed):
        return bcrypt.checkpw(password.encode(), hashed.encode())