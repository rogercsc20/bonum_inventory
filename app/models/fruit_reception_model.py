from app.extensions import db
from sqlalchemy import Enum, ForeignKey
from datetime import datetime

class FruitReception(db.Model):
    __tablename__ = "fruit_reception"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=True, default=datetime.today)
    time = db.Column(db.DateTime, nullable=False)
    product = db.Column(db.String(50), nullable=False)
    presentation = db.Column(
        Enum("1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz", name="presentation"),
        nullable=False)
    box_quantity = db.Column(db.Integer, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)

    client_id = db.Column(db.Integer, ForeignKey("clients.id"), nullable=False)
    client = db.relationship("Client", back_populates="fruit_receptions")

    def __repr__(self):
        return f"<FruitReception {self.fruta} for Client {self.client_id}>"