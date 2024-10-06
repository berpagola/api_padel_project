from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.pareja import Pareja
from app.models.jugador import Jugador
from app.schemas.pareja import ParejaCreate
from app.schemas.jugador import JugadorCreate
import logging

logger = logging.getLogger(__name__)

class CRUDPareja(CRUDBase[Pareja, ParejaCreate, ParejaCreate]):
    def get_or_create(self, db: Session, *, obj_in: ParejaCreate) -> Pareja:
        # Buscar si la pareja ya existe
        pareja = db.query(Pareja).filter(
            ((Pareja.jugador1_id == obj_in.jugador1_id) & (Pareja.jugador2_id == obj_in.jugador2_id)) |
            ((Pareja.jugador1_id == obj_in.jugador2_id) & (Pareja.jugador2_id == obj_in.jugador1_id))
        ).first()
        
        if pareja:
            return pareja
        
        # Si no existe, crear la pareja
        db_obj = Pareja(
            jugador1_id=obj_in.jugador1_id,
            jugador2_id=obj_in.jugador2_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_with_jugadores(self, db: Session, *, jugador1: JugadorCreate, jugador2: JugadorCreate) -> Pareja:
        # Buscar o crear jugador1
        db_jugador1 = db.query(Jugador).filter(
            Jugador.nombre == jugador1.nombre,
            Jugador.apellido == jugador1.apellido
        ).first()
        if not db_jugador1:
            logger.info(f"Creating new jugador: {jugador1.nombre} {jugador1.apellido}")
            db_jugador1 = Jugador(**jugador1.dict())
            db.add(db_jugador1)
        else:
            logger.info(f"Found existing jugador: {jugador1.nombre} {jugador1.apellido}")

        # Buscar o crear jugador2
        db_jugador2 = db.query(Jugador).filter(
            Jugador.nombre == jugador2.nombre,
            Jugador.apellido == jugador2.apellido
        ).first()
        if not db_jugador2:
            logger.info(f"Creating new jugador: {jugador2.nombre} {jugador2.apellido}")
            db_jugador2 = Jugador(**jugador2.dict())
            db.add(db_jugador2)
        else:
            logger.info(f"Found existing jugador: {jugador2.nombre} {jugador2.apellido}")

        db.flush()  # Para asegurarnos de que los jugadores tengan IDs

        # Buscar si la pareja ya existe
        existing_pareja = db.query(Pareja).filter(
            ((Pareja.jugador1_id == db_jugador1.id) & (Pareja.jugador2_id == db_jugador2.id)) |
            ((Pareja.jugador1_id == db_jugador2.id) & (Pareja.jugador2_id == db_jugador1.id))
        ).first()

        if existing_pareja:
            logger.info(f"Found existing pareja: {db_jugador1.nombre} {db_jugador1.apellido} - {db_jugador2.nombre} {db_jugador2.apellido}")
            return existing_pareja

        # Si la pareja no existe, crearla
        logger.info(f"Creating new pareja: {db_jugador1.nombre} {db_jugador1.apellido} - {db_jugador2.nombre} {db_jugador2.apellido}")
        pareja = Pareja(jugador1_id=db_jugador1.id, jugador2_id=db_jugador2.id)
        db.add(pareja)
        db.flush()
        return pareja

pareja = CRUDPareja(Pareja)