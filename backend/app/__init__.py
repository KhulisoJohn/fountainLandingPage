from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
load_dotenv()

from app.config.db import Config 

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
def create_app():

    load_dotenv()

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    with app.app_context():
        from sqlalchemy import text
        db.session.execute(text("SELECT 1"))
        print("Database connected successfully!")

    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.route("/")
    def home():
        return {"message": "Backend running successfully"}

    return app