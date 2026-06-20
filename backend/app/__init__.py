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

        # ---------------- DB INIT ----------------
        db.init_app(app)
        logger.info("DB_INITIALIZED")

        with app.app_context():
            db.session.execute(text("SELECT 1"))
            logger.info("DATABASE_CONNECTED")

            # IMPORTANT: ensure models are registered
            from app.Modules.User.user import User
            from app.Modules.Authentication.pending_user import PendingUser
            from app.Modules.Prayer.prayer import Prayer
            from app.Modules.Event.event import Event
            from app.Modules.Sermon.sermon import Sermon

        # ---------------- JWT ----------------
        jwt.init_app(app)
        logger.info("JWT_INITIALIZED")

        # ---------------- MIGRATION ----------------
        migrate.init_app(app, db)
        logger.info("MIGRATION_INITIALIZED")

        # ---------------- BLUEPRINTS ----------------
        from app.Modules.Authentication.route import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
        logger.info("AUTH_BLUEPRINT_REGISTERED")

        from app.Modules.User.route import user_bp
        app.register_blueprint(user_bp, url_prefix="/api/user")
        logger.info("USER_BLUEPRINT_REGISTERED")

        from app.Modules.Event.route import event_bp
        app.register_blueprint(event_bp, url_prefix="/api/events")
        logger.info("EVENT_BLUEPRINT_REGISTERED")

        from app.Modules.Prayer.route import prayer_bp
        app.register_blueprint(prayer_bp, url_prefix="/api/prayers")
        logger.info("PRAYER_BLUEPRINT_REGISTERED")

        from app.Modules.Sermon.route import sermon_bp
        app.register_blueprint(sermon_bp, url_prefix="/api/sermons")
        logger.info("SERMON_BLUEPRINT_REGISTERED")

        from app.Modules.Testimonial.route import testimonial_bp
        app.register_blueprint(testimonial_bp, url_prefix="/api/testimonials")
        logger.info("TESTIMONIAL_BLUEPRINT_REGISTERED")

        # ---------------- ROOT ROUTES ----------------
        @app.route("/")
        def home():
            logger.info("HEALTH_CHECK_REQUEST")
            return {"message": "Backend running successfully"}

        @app.route("/health")
        def health():
            logger.info("HEALTH_CHECK_REQUEST")
            return {
                "status": "healthy",
                "message": "Backend running successfully"
            }, 200

        logger.info("APPLICATION_READY")

        return app

    except Exception as e:
        logger.error(f"APPLICATION_STARTUP_FAILED | error={str(e)}")
        raise