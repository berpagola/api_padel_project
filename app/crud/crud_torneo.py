from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.torneo import Torneo
from app.schemas.torneo import TorneoCreate, TorneoUpdate
from fastapi import HTTPException

class CRUDTorneo(CRUDBase[Torneo, TorneoCreate, TorneoUpdate]):
    def get_by_nombre(self, db: Session, *, nombre: str) -> Torneo:
        return db.query(Torneo).filter(Torneo.nombre == nombre).first()

    def create_or_update(self, db: Session, *, obj_in: TorneoCreate) -> Torneo:
        existing_torneo = self.get_by_nombre(db, nombre=obj_in.nombre)
        if existing_torneo:
            # Si el torneo existe, actualizamos sus datos
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(existing_torneo, field, value)
            db.add(existing_torneo)
            db.commit()
            db.refresh(existing_torneo)
            return existing_torneo
        else:
            # Si el torneo no existe, lo creamos
            db_obj = Torneo(**obj_in.dict())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

torneo = CRUDTorneo(Torneo)