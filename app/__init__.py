from flask import Flask
from app.logger import setup_logger
from config import Config
from app.extensions import db, migrate, jwt
from app.routes.user_routes import user_blp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    #Set up logger
    setup_logger()

    app.register_blueprint(user_blp)

    return app
