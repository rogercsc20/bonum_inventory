from marshmallow import Schema, fields, ValidationError, validates

class InventorySchema(Schema):
    id = fields.Int(dump_only=True)
    inventory_type = fields.Str(required=True)
    product = fields.Str(required=True)
    presentation = fields.Str(required=True)
    box_quantity = fields.Int(required=True)

    @validates("inventory_type")
    def validate_inventory_type(self, value):
        allowed_values = ["initial", "final"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid inventory_type: {value}. Must be 'initial' or 'final'.")

    @validates("fruta")
    def validate_product(self, value):
        allowed_values = ["fresa", "frambuesa", "zarzamora", "arandano"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid product: {value}. Must be one of {allowed_values}.")

    @validates("presentation")
    def validate_presentation(self, value):
        allowed_values = ["1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid presentation: {value}. Must be one of {allowed_values}.")
