from app.extensions import db
from  sqlalchemy import Enum

class FruitReception(db.Model):
    __tablename__ = "fruit_reception"

    id = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.DateTime, nullable=False)
    fruta = db.Column(db.String(50), nullable=False)
    presentacion = db.Column(
        Enum("1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz", name="presentacion"),
        nullable=False)
    cantidad_cajas = db.Column(db.Integer, nullable=False)
