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

# Create Blueprint
user_blp = Blueprint("user", "user", url_prefix="/api/user", description="Operations on users")


@user_blp.route("/register")
class RegisterUser(MethodView):
    @user_blp.arguments(UserSchema)
    @user_blp.response(201, UserSchema)
    def post(self, data):
        """Register a new user"""
        try:
            # Check if email or username already exists
            if User.query.filter_by(email=data["email"]).first() or User.query.filter_by(username=data["username"]).first():
                return {"message": "User already exists"}, 400

            # Create new user
            new_user = User(
                name=data["name"],
                email=data["email"],
                username=data["username"],
                role=data.get("role", "user")  # Default role: user
            )
            new_user.set_password(data["password"])  # Hash the password

            db.session.add(new_user)
            db.session.commit()

            return new_user
        except Exception as e:
            db.session.rollback()
            return {"error": f"An error occurred: {str(e)}"}, 500


@user_blp.route("/login")
class LoginUser(MethodView):
    @user_blp.arguments(UserSchema(partial=True))
    def post(self, data):
        """Login a user and return an access token"""
        try:
            user = User.query.filter_by(email=data["email"]).first()
            if user and user.check_password(data["password"]):
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))
                return {"access_token": access_token, "refresh_token" : refresh_token}, 200
            return {"message": "Invalid email or password"}, 401
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500


@user_blp.route("/logout")
class LogoutUser(MethodView):
    @jwt_required()
    def post(self):
        """Logout a user by revoking their token"""
        try:
            jti = get_jwt()["jti"]  # JWT ID
            db.session.add(TokenBlocklist(jti=jti, created_at=datetime.utcnow()))
            db.session.commit()
            return {"message": "Token revoked successfully"}, 200
        except Exception as e:
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
