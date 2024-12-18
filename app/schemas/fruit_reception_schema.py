from marshmallow import Schema, fields, validates, ValidationError


class FruitReceptionSchema(Schema):
    id = fields.Int(dump_only=True)
    hora = fields.DateTime(required=True)
    fruta = fields.Str(required=True)
    presentacion = fields.Str(required=True)
    cantidad_cajas = fields.Int(required=True)

    @validates("fruta")
    def validate_fruta(self, value):
        allowed_values = ["fresa", "frambuesa", "zarzamora", "arandano"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid fruta: {value}. Must be one of {allowed_values}.")

    @validates("presentation")
    def validate_presentation(self, value):
        allowed_values = ["1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid presentation: {value}. Must be one of {allowed_values}.")
