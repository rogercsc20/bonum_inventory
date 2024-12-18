from flask.views import MethodView
from flask_smorest import Blueprint
from app.extensions import db
from app.models.user_model import User
from app.models.token_blocklist_model import TokenBlocklist
from app.schemas.user_schema import UserSchema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from datetime import datetime
import logging


logger = logging.getLogger(__name__)
user_blp = Blueprint("user", "user", url_prefix="/user", description="Operations on users")


@user_blp.route("/register")
class RegisterUser(MethodView):
    @user_blp.arguments(UserSchema)
    @user_blp.response(201, UserSchema)
    def post(self, data):
        """Register a new user"""
        try:
            logger.info(f"Attempting to register user: {data["username"]}")
            # Check if email or username already exists
            if User.query.filter_by(email=data["email"]).first():
                logger.warning(f"Email already in use: {data['email']}")
                return {"message" : "An account with this email is already registered"}
            if User.query.filter_by(username=data["username"]).first():
                return {"message": "Username already exists"}, 400

            # Create new user
            new_user = User(
                name=data["name"],
                email=data["email"],
                username=data["username"],
                role=data.get("role", "user")
            )
            new_user.set_password(data["password"])

            db.session.add(new_user)
            db.session.commit()

            return new_user
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            db.session.rollback()
            return {"error": f"An error occurred: {str(e)}"}, 500


@user_blp.route("/login")
class LoginUser(MethodView):
    @user_blp.arguments(UserSchema(partial=True))
    def post(self, data):
        """Login a user and return an access token"""
        try:
            logger.info(f"User {data['username']} is logging in")
            user = User.query.filter_by(username=data["username"]).first()
            if user and user.check_password(data["password"]):
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))
                logger.info(f"User {data['username']} logged in successfully")
                return {"access_token": access_token, "refresh_token" : refresh_token}, 200
            return {"message": "Invalid email or password"}, 401
        except Exception as e:
            logger.error(f"Error logging in for user: {data['username']}. {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}, 500


@user_blp.route("/logout")
class LogoutUser(MethodView):
    @jwt_required()
    def post(self):
        """Logout a user by revoking their token"""
        try:
            logger.info("User logging out")
            jti = get_jwt()["jti"]  # JWT ID
            db.session.add(TokenBlocklist(jti=jti, created_at=datetime.utcnow()))
            db.session.commit()
            logger.info("User logged out")
            return {"message": "Token revoked successfully"}, 200
        except Exception as e:
            logger.error(f"Error logging out: {str(e)}")
            db.session.rollback()
            return {"error": f"An error occurred: {str(e)}"}, 500


@user_blp.route("/protected")
class ProtectedRoute(MethodView):
    @jwt_required()
    def get(self):
        """Protected route example"""
        try:
            current_user = get_jwt_identity()
            return {"message": f"Hello, user {current_user}!"}, 200
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500
