from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.extensions import db

class Ticket(db.Model):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True)
    fecha_emision = Column(DateTime, nullable=False, server_default=func.now())
    numero_pedido = Column(Integer, nullable=True)
    descuento = Column(Numeric(10, 2), nullable=False, default=0)
    total = Column(Numeric(10, 2), nullable=False)
    efectivo_recibido = Column(Numeric(10, 2), nullable=False)
    cambio = Column(Numeric(10, 2), nullable=False)
    emitido_por = Column(Integer, nullable=False)

    venta_id = Column(Integer, ForeignKey("venta.id"), nullable=False)
    venta = relationship("Venta", backref="ticket")

    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=True)
    cliente = relationship("Cliente")

    def __repr__(self):
        return f"Ticket #{self.id}"