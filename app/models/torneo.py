from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db.base import Base

class Torneo(Base):
    __tablename__ = "torneos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    ubicacion = Column(String)

    partidos = relationship("Partido", back_populates="torneo")
