from app.extensions import db
from sqlalchemy import Column, Integer, String, Text

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)

    def __repr__(self):
        return self.nombre