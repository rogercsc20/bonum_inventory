from marshmallow import Schema, fields, ValidationError, validates

class InventorySchema(Schema):
    id = fields.Int(dump_only=True)
    inventory_type = fields.Str(required=True)
    fruta = fields.Str(required=True)
    presentacion = fields.Str(required=True)
    cantidad_cajas = fields.Int(required=True)

    @validates("inventory_type")
    def validate_inventory_type(self, value):
        allowed_values = ["initial", "final"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid inventory_type: {value}. Must be 'initial' or 'final'.")

    @validates("fruta")
    def validate_fruta(self, value):
        allowed_values = ["fresa", "frambuesa", "zarzamora", "arandano"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid fruta: {value}. Must be one of {allowed_values}.")

    @validates("presentacion")
    def validate_presentacion(self, value):
        allowed_values = ["1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid presentacion: {value}. Must be one of {allowed_values}.")
