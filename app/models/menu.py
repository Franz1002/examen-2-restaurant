from sqlalchemy import Column, ForeignKey, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship
from app.extensions import db

class Menu(db.Model):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    detalle = Column(Text, nullable=True)
    img = Column(String(150), nullable=True)
    estado = Column(Integer, nullable=False, default=1)

    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    categoria = relationship("Categoria", backref="menus")

    def __repr__(self):
        return self.nombre