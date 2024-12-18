from marshmallow import Schema, fields, validates, ValidationError


class InOutPrecoolingSchema(Schema):
    id = fields.Int(dump_only=True)
    fruta = fields.Str(required=True)
    presentacion = fields.Str(required=True)
    tipo_fruta = fields.Str(required=True)
    numero_pallet = fields.Int(required=True)
    cantidad_cajas = fields.Int(required=True)
    codigo_tarima = fields.Str(required=True)
    cuarto = fields.Str(required=True)
    hora_entrada = fields.DateTime(required=True)
    temperatura_entrada = fields.Str(required=True)
    hora_salida = fields.DateTime(required=True)
    temperatura_salida = fields.Str(required=True)
    tiempo_total = fields.TimeDelta(dump_only=True)

    @validates("fruta")
    def validate_fruta(self, value):
        allowed_values = ["fresa", "frambuesa", "zarzamora", "arandano"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid fruta: {value}. Must be one of {allowed_values}.")

    @validates("tipo_fruta")
    def validate_tipo_fruta(self, value):
        allowed_values = ["convencional", "organica"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid tipo_fruta: {value}. Must be one of {allowed_values}.")
