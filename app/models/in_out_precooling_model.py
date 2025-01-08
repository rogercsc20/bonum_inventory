from app.extensions import db
from sqlalchemy import Enum, ForeignKey
from datetime import timedelta, datetime


class InOutPrecooling(db.Model):
    __tablename__ = "in_out_precooling"

    client_id = db.Column(db.Integer, ForeignKey("clients.id"), nullable=False)
    client = db.relationship("Client", back_populates="in_out_precoolings")

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=True, default=datetime.today)
    product = db.Column(
        Enum("fresa", "frambuesa", "zarzamora", "arandano", name="product"),
        nullable=False
    )
    presentation = db.Column(
        Enum("1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz", name="presentation"),
        nullable=False
    )
    fruit_type = db.Column(
        Enum("convencional", "organica", name="fruit_type"),
        nullable=True, default="convencional"
    )
    pallet_quantity = db.Column(db.Integer, nullable=True)
    box_quantity = db.Column(db.Integer, nullable=False)
    pallet_code = db.Column(db.String(20), nullable=True)
    room_number = db.Column(db.String(20), nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False)
    entry_temperature = db.Column(db.Float, nullable=True)
    exit_time = db.Column(db.DateTime, nullable=True)
    exit_temperature = db.Column(db.Float, nullable=True)
    client_name = db.Column(db.String(100), nullable=False)


    @property
    def total_time(self):
        """Calculate time spent in pre-cooling."""
        if self.entry_time and self.exit_time:
            return self.exit_time - self.entry_time
        return timedelta(0)

    def __repr__(self):
        return f"<InOutPrecooling {self.product} for Client {self.client_id}>"

