from pydantic import BaseModel

class JugadorBase(BaseModel):
    nombre: str
    apellido: str
    nacionalidad: str = None

class JugadorCreate(JugadorBase):
    pass

class JugadorUpdate(JugadorBase):
    pass

class Jugador(JugadorBase):
    id: int

    class Config:
        orm_mode = True