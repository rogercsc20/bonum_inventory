from marshmallow import Schema, fields, validates, ValidationError

class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    email = fields.Email(required=False)
    address = fields.Str(required=False)
    invoice_details = fields.Str(required=False)
    price_per_box = fields.Float(required=True)
    additional_charges = fields.Float(required=False)

    # Relationship fields (dump_only for serializing)
    fruit_receptions = fields.Nested("FruitReceptionSchema", many=True, dump_only=True)
    in_out_precoolings = fields.Nested("InOutPrecoolingSchema", many=True, dump_only=True)

    @validates("price_per_box")
    def validate_price_per_box(self, value):
        if value < 0:
            raise ValidationError("Price per box must be non-negative.")

    @validates("additional_charges")
    def validate_additional_charges(self, value):
        if value < 0:
            raise ValidationError("Additional charges must be non-negative.")
