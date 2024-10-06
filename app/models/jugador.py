from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    nacionalidad = Column(String)
