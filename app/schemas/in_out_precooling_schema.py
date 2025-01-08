from marshmallow import Schema, fields, validates, ValidationError, pre_load
from datetime import datetime


class InOutPrecoolingSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=False, missing=datetime.today().date)
    product = fields.Str(required=True)
    presentation = fields.Str(required=True)
    fruit_type = fields.Str(required=False, missing="convencional")
    pallet_quantity = fields.Int(required=False)
    box_quantity = fields.Int(required=True)
    pallet_code = fields.Str(required=True)
    room_number = fields.Str(required=True)
    entry_time = fields.DateTime(required=True)
    entry_temperature = fields.Float(required=False)
    exit_time = fields.DateTime(required=False)
    exit_temperature = fields.Float(required=False)
    total_time = fields.TimeDelta(dump_only=True)
    client_name = fields.Str(required=True)

    @validates("product")
    def validate_product(self, value):
        allowed_values = ["fresa", "frambuesa", "zarzamora", "arandano"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid product: {value}. Must be one of {allowed_values}.")

    @validates("fruit_type")
    def validate_fruit_type(self, value):
        allowed_values = ["convencional", "organica"]
        if value not in allowed_values:
            raise ValidationError(f"Invalid fruit type: {value}. Must be one of {allowed_values}.")

    @pre_load
    def parse_inputs(self, data, **kwargs):
        """
        Handle parsing for `date`, `entry_time`, and `exit_time`.
        """
        if "fruit_type" not in data or not data["fruit_type"]:
            data["fruit_type"] = "convencional"

        if "date" not in data or not data["date"]:
            data["date"] = datetime.today().date().strftime("%Y-%m-%d")
        else:
            try:
                data["date"] = datetime.strptime(data["date"], "%d/%m/%y").date()
            except ValueError:
                raise ValidationError("Invalid date format. Use 'DD/MM/YY'.")

        # Parse times
        for field in ["entry_time", "exit_time"]:
            if field in data:
                try:
                    if data[field] == "now":
                        data[field] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        input_time = datetime.strptime(data[field], "%H:%M").time()
                        today = datetime.now().date()
                        data[field] = datetime.combine(today, input_time).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    raise ValidationError(f"Invalid time format for {field}. Use 'HH:MM' or 'now'.")
        return data
