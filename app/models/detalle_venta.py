from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from app.extensions import db

class DetalleVenta(db.Model):
    __tablename__ = "detalle_venta"
    id = Column(Integer, primary_key=True)

    venta_id = Column(Integer, ForeignKey("venta.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=False)

    cantidad = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    venta = relationship("Venta", backref="detalles")
    menu = relationship("Menu")

    def __repr__(self):
        return f"{self.cantidad} x {self.menu.nombre if self.menu else ''}"