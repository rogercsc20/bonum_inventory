from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Email

class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # Output only
    name = fields.Str(required=True, validate=Length(min=2, max=100))
    email = fields.Email(required=True, validate=Email())
    username = fields.Str(required=True, validate=Length(min=3, max=50))
    password = fields.Str(
        required=True,
        validate=Length(min=6, max=256),
        load_only=True
    )
    role = fields.Str(required=True, default="user")

    @validates("role")
    def validate_role(self, value):
        allowed_roles = ["user", "manager", "admin"]
        if value not in allowed_roles:
            raise ValidationError(f"Invalid role: {value}. Allowed roles: {allowed_roles}.")
