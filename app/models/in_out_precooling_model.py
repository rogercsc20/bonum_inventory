from app.extensions import db
from sqlalchemy import Enum
from datetime import timedelta

class InOutPrecooling(db.Model):
    __tablename__ = "in_out_precooling"

    id = db.Column(db.Integer, primary_key=True)
    fruta = db.Column(
        Enum("fresa", "frambuesa", "zarzamora", "arandano", name="fruta_type"),
        nullable=False)
    presentacion = db.Column(
        Enum("1lb", "2lb", "4.4oz", "6oz", "8.8oz", "11oz", "12oz", name="presentacion"),
        nullable=False)
    tipo_fruta = db.Column(Enum("convencional", "organica", name="tipo_fruta"), nullable=False)

    numero_pallet = db.Column(db.Integer, nullable=False)
    cantidad_cajas = db.Column(db.Integer, nullable=False)
    codigo_tarima = db.Column(db.String(20), nullable=False)
    cuarto = db.Column(db.String(20), nullable=False)
    hora_entrada = db.Column(db.DateTime, nullable=False)
    temperatura_entrada = db.Column(db.String(20), nullable=False)
    hora_salida = db.Column(db.DateTime, nullable=False)
    temperatura_salida = db.Column(db.String(20), nullable=False)


    @property
    def tiempo_total(self):
        """Calculate time spent in pre-cooling."""
        if self.hora_entrada and self.hora_salida:
            return self.hora_salida - self.hora_entrada
        return timedelta(0)

    def __repr__(self):
        return f"<InOutPrecooling {self.fruta} {self.numero_pallet}>"