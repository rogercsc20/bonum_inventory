from marshmallow import Schema, fields
from datetime import datetime


class ShippingManifestSchema(Schema):
    id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)

    client_name = fields.Str(required=True)
    date = fields.Date(required=False, missing=datetime.today().date)

    product = fields.Str(required=True)
    presentation = fields.Str(required=True)
    fruit_type = fields.Str(required=True)
    box_quantity_per_pallet = fields.Int(required=True)

    truck_plates = fields.Str(required=True)
    container_plates = fields.Str(required=True)
    container_temperature = fields.Float(required=True)

    fruit_in_condition = fields.Str(required=True)
    clean_without_odor = fields.Str(required=True)
    plague_presence = fields.Str(required=True)

    last_load_product = fields.Str(required=False)
    pallet_mount = fields.Str(required=True)
    strapping = fields.Str(required=True)
    load_distribution = fields.Str(required=True)

    arrival_time = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    load_time = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    exit_time = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    total_duration = fields.TimeDelta(dump_only=True)
    total_cost = fields.Float(dump_only=True)

    stamp_number = fields.Str(required=False)
    chismograph_number = fields.Str(required=False)

    bonum_representative = fields.Str(required=True)
    client_representative = fields.Str(required=False)
    driver_name = fields.Str(required=True)
    carrier_company = fields.Str(required=True)

    total1 = fields.Str(required=False)
    total2 = fields.Str(required=False)
    total3 = fields.Str(required=False)
    total4 = fields.Str(required=False)
    total5 = fields.Str(required=False)
    total6 = fields.Str(required=False)