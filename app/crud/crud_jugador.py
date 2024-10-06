from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jugador import Jugador
from app.schemas.jugador import JugadorCreate, JugadorUpdate

class CRUDJugador(CRUDBase[Jugador, JugadorCreate, JugadorUpdate]):
    def get_by_nombre_apellido(self, db: Session, *, nombre: str, apellido: str):
        return db.query(Jugador).filter(Jugador.nombre == nombre, Jugador.apellido == apellido).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(Jugador).offset(skip).limit(limit).all()

jugador = CRUDJugador(Jugador)