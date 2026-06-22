from sqlalchemy import Column, DateTime, Integer, Numeric
from sqlalchemy.sql import func
from app.extensions import db

class Venta(db.Model):
    __tablename__ = "venta"
    id = Column(Integer, primary_key=True)
    fecha_venta = Column(DateTime, nullable=False, server_default=func.now())
    total_venta = Column(Numeric(10, 2), nullable=False, default=0)
    usuario_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Venta #{self.id}"