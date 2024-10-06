from pydantic import BaseModel
from datetime import date

class TorneoBase(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    ubicacion: str

class TorneoCreate(TorneoBase):
    pass

class TorneoUpdate(TorneoBase):
    pass

class Torneo(TorneoBase):
    id: int

    class Config:
        orm_mode = True