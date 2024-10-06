from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Pareja(Base):
    __tablename__ = "parejas"

    id = Column(Integer, primary_key=True, index=True)
    jugador1_id = Column(Integer, ForeignKey("jugadores.id"))
    jugador2_id = Column(Integer, ForeignKey("jugadores.id"))

    jugador1 = relationship("Jugador", foreign_keys=[jugador1_id])
    jugador2 = relationship("Jugador", foreign_keys=[jugador2_id])
