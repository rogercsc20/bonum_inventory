from app.extensions import db

class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    address = db.Column(db.String(180), nullable=True)
    invoice_details = db.Column(db.String(100), nullable=True)
    price_per_box = db.Column(db.Float, nullable=False)
    additional_charges = db.Column(db.Float, nullable=True, default=0, server_default="0")

    # Relationships
    fruit_receptions = db.relationship("FruitReception", back_populates="client")
    in_out_precoolings = db.relationship("InOutPrecooling", back_populates="client")
    shipping_manifests = db.relationship("ShippingManifest", back_populates="client")

    def __repr__(self):
        return f"<Client {self.name}>"

    def calculate_total_price(self, box_count, hours):
        """
        Calculate the total price based on the number of boxes and hours.
        :param box_count: Number of boxes.
        :param hours: Hours in storage.
        :return: Total price as float.
        """
        if box_count < 0 or hours < 0:
            raise ValueError("Box count and hours must be non-negative.")
        return (self.price_per_box * hours * box_count) + (self.additional_charges or 0)
