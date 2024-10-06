from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .jugador import Jugador, JugadorCreate
from .torneo import Torneo
from .pareja import Pareja

class EquipoCreate(BaseModel):
    jugadores: List[JugadorCreate]

class PartidoBase(BaseModel):
    fecha: str
    cancha: str
    horario_inicio_cancha: str
    hora_local_actual: str
    horario: str
    tipo_horario: str
    round: str
    sets1: List[str]
    sets2: List[str]
    estado: str
    hora_buenos_aires: str
    es_despues_partido_anterior: bool

class PartidoCreate(PartidoBase):
    equipo1: EquipoCreate
    equipo2: EquipoCreate
    torneo_id: int

class PartidoCreateDB(PartidoBase):
    equipo1_id: int
    equipo2_id: int
    torneo_id: int

class PartidoUpdate(PartidoBase):
    equipo1_id: Optional[int] = None
    equipo2_id: Optional[int] = None

class Partido(PartidoBase):
    id: int
    equipo1: Pareja
    equipo2: Pareja
    torneo: Torneo
    horario_inicio_cancha_utc: Optional[datetime] = None
    hora_local_actual_utc: Optional[datetime] = None
    hora_buenos_aires_utc: Optional[datetime] = None

    class Config:
        orm_mode = True

class PartidoList(BaseModel):
    partidos: List[PartidoCreate]