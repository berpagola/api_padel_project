from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ARRAY, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String)
    cancha = Column(String)
    horario_inicio_cancha = Column(String)
    hora_local_actual = Column(String)
    horario = Column(String)
    tipo_horario = Column(String)
    round = Column(String)
    estado = Column(String)
    hora_buenos_aires = Column(String)
    
    sets1 = Column(ARRAY(String))
    sets2 = Column(ARRAY(String))

    horario_inicio_cancha_utc = Column(DateTime, nullable=True)
    hora_local_actual_utc = Column(DateTime, nullable=True)
    hora_buenos_aires_utc = Column(DateTime, nullable=True)
    es_despues_partido_anterior = Column(Boolean, default=False)

    torneo_id = Column(Integer, ForeignKey("torneos.id"), nullable=False)
    equipo1_id = Column(Integer, ForeignKey("parejas.id"), nullable=True)
    equipo2_id = Column(Integer, ForeignKey("parejas.id"), nullable=True)

    torneo = relationship("Torneo", back_populates="partidos")
    equipo1 = relationship("Pareja", foreign_keys=[equipo1_id])
    equipo2 = relationship("Pareja", foreign_keys=[equipo2_id])