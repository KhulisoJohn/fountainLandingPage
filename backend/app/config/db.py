import os

class Config:

    # DATABASE (Supabase / Postgres)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # SAFETY
    PROPAGATE_EXCEPTIONS = True