from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from app.extensions import db

class Cliente(db.Model):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)    
    documento = Column(String(20), nullable=True, unique=True)
    celular = Column(String(20), nullable=True, unique=True)
    fecha_registro = Column(DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return self.nombre