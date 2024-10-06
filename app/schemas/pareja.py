from pydantic import BaseModel
from .jugador import Jugador

class ParejaBase(BaseModel):
    jugador1_id: int
    jugador2_id: int

class ParejaCreate(ParejaBase):
    pass

class ParejaUpdate(ParejaBase):
    pass

class Pareja(ParejaBase):
    id: int
    jugador1: Jugador
    jugador2: Jugador

    class Config:
        orm_mode = True