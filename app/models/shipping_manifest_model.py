from app.extensions import db
from sqlalchemy import Enum, ForeignKey
from datetime import datetime


class ShippingManifest(db.Model):
    __tablename__ = "shipping_manifest"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey("clients.id"), nullable=False)
    client = db.relationship("Client", back_populates="shipping_manifests")

    client_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=True, default=datetime.today)

    # Shipping Details
    product = db.Column(db.String(50), nullable=False)
    presentation = db.Column(
        Enum("1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz", name="presentation_shipping"),
        nullable=False)
    fruit_type = db.Column(Enum("convencional", "organica", name="fruit_type_shipping"), nullable=False)
    box_quantity_per_pallet = db.Column(db.Integer, nullable=False)
    truck_plates = db.Column(db.String(20), nullable=False)
    container_plates = db.Column(db.String(20), nullable=False)
    container_temperature = db.Column(db.Float, nullable=False)

    # Load Details
    fruit_in_condition = db.Column(Enum("yes", "no", name="fruit_condition"), nullable=False)
    clean_without_odor = db.Column(Enum("yes", "no", name="clean_without_odor"), nullable=False)
    plague_presence = db.Column(Enum("yes", "no", name="plague_presence"), nullable=False)
    last_load_product = db.Column(db.String(100), nullable=True)
    pallet_mount = db.Column(Enum("good", "bad", name="pallet_mount"), nullable=False)
    strapping = db.Column(Enum("good", "bad", name="strapping"), nullable=False)
    load_distribution = db.Column(Enum("good", "bad", name="load_distribution"), nullable=False)

    # Time Tracking
    arrival_time = db.Column(db.DateTime, nullable=False)
    load_time = db.Column(db.DateTime, nullable=False)
    exit_time = db.Column(db.DateTime, nullable=True)

    stamp_number = db.Column(db.String(60), nullable=True)
    chismograph_number = db.Column(db.String(60), nullable=True)

    # Total Time and Costs
    total_duration = db.Column(db.Interval, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    # Representatives
    bonum_representative = db.Column(db.String(100), nullable=False)
    client_representative = db.Column(db.String(100), nullable=True)
    driver_name = db.Column(db.String(100), nullable=False)
    carrier_company = db.Column(db.String(100), nullable=False)

    # Totals for Each Fruit Type
    total1 = db.Column(db.String, nullable=True)
    total2 = db.Column(db.String, nullable=True)
    total3 = db.Column(db.String, nullable=True)
    total4 = db.Column(db.String, nullable=True)
    total5 = db.Column(db.String, nullable=True)
    total6 = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<ShippingManifest for Client {self.client_id}>"
