from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from app.models.user_model import User

def role_required(*roles):
    """
    A decorator to restrict access to routes based on user roles.
    :param roles: List of roles allowed to access the route (e.g., "user", "manager", "admin").
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)

            if not user:
                return jsonify({"message": "User not found"}), 404

            if user.role not in roles:
                return jsonify({"message": "Access denied: insufficient permissions"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
