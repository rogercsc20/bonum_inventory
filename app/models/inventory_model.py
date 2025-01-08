from app.extensions import db
from sqlalchemy import Enum

class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    inventory_type = db.Column(Enum("initial", "final", name="inventory_type"), nullable=False)
    product = db.Column(Enum("fresa", "frambuesa", "zarzamora", "arandano", name="fruta_type"), nullable=False)
    presentation = db.Column(
        Enum("1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz", name="presentation"),
        nullable=False)
    box_quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Inventory {self.inventory_type} {self.product} {self.presentation}>"
