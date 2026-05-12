from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import text

import os

from app.config.db import Config
from app.utils.logger import logger

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app():

    logger.info("APPLICATION_STARTUP")

    try:
        load_dotenv()
        logger.info("ENV_LOADED")

        app = Flask(__name__)
        app.config.from_object(Config)

        logger.info("CONFIG_LOADED")

        CORS(app)

        db.init_app(app)
        logger.info("DB_INITIALIZED")

        # Test DB connection
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            logger.info("DATABASE_CONNECTED")

        jwt.init_app(app)
        logger.info("JWT_INITIALIZED")

        migrate.init_app(app, db)
        logger.info("MIGRATION_INITIALIZED")

        # Blueprints
        from app.routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
        logger.info("AUTH_BLUEPRINT_REGISTERED")

        @app.route("/")
        def home():
            logger.info("HEALTH_CHECK_REQUEST")
            return {"message": "Backend running successfully"}

        logger.info("APPLICATION_READY")

        return app

    except Exception as e:
        logger.error(f"APPLICATION_STARTUP_FAILED | error={str(e)}")
        raise