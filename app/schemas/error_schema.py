from marshmallow import Schema, fields

class ErrorSchema(Schema):
    message = fields.Str(required=True)
