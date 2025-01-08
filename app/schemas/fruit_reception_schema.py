from marshmallow import Schema, fields, validates, ValidationError, pre_load
from datetime import datetime


class FruitReceptionSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=False, missing=datetime.today().date)
    time = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    product = fields.Str(required=True)
    presentation = fields.Str(required=True)
    box_quantity = fields.Int(required=True)
    client_name = fields.Str(required=True)

    @validates("product")
    def validate_product(self, value):
        allowed_values = ["fresa", "frambuesa", "zarzamora", "arandano"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid product: {value}. Must be one of {allowed_values}.")

    @validates("box_quantity")
    def validate_box_quantity(self, value):
        if value <= 0:
            raise ValidationError("Box quantity must be a positive integer.")

    @validates("presentation")
    def validate_presentation(self, value):
        allowed_values = ["1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid presentation: {value}. Must be one of {allowed_values}.")

    @pre_load
    def parse_inputs(self, data, **kwargs):
        """
        Handle parsing for `date` and `time` fields to allow simpler inputs.
        """
        # Parse date
        if "date" in data and data["date"]:
            try:
                data["date"] = datetime.strptime(data["date"], "%d/%m/%y").date()
            except ValueError:
                raise ValidationError("Invalid date format. Use 'DD/MM/YY'.")

        # Parse time
        if "time" in data:
            try:
                if data["time"] == "now":
                    data["time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                else:
                    # Parse "HH:MM" and combine with today's date
                    input_time = datetime.strptime(data["time"], "%H:%M").time()
                    today = data["date"] if "date" in data else datetime.now().date()
                    data["time"] = datetime.combine(today, input_time).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValidationError("Invalid time format. Use 'HH:MM' or 'now'.")
        return data