from app.extensions import db
from sqlalchemy import Enum

class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    inventory_type = db.Column(Enum("initial", "final", name="inventory_type"), nullable=False)
    fruta = db.Column(Enum("fresa", "frambuesa", "zarzamora", "arandano", name="fruta_type"), nullable=False)
    presentacion = db.Column(
        Enum("1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz", name="presentacion"),
        nullable=False)
    cantidad_cajas = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Inventory {self.inventory_type} {self.fruta} {self.presentation}>"
