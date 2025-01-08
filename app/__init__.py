from flask import Flask
from app.logger import setup_logger
from config import Config
from app.extensions import db, migrate, jwt
from app.routes.user_routes import user_blp
from app.routes.fruit_reception_routes import fruit_reception_blp
from app.routes.in_out_precooling_routes import in_out_precooling_blp
from app.routes.client_routes import client_blp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    #Set up logger
    setup_logger()

    # Register blueprints
    app.register_blueprint(user_blp)
    app.register_blueprint(fruit_reception_blp)
    app.register_blueprint(in_out_precooling_blp)
    app.register_blueprint(client_blp)

    return app

