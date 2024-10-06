from typing import List, Union, Dict, Any
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.partido import Partido as PartidoModel
from app.models.pareja import Pareja
from app.schemas.partido import PartidoCreate, PartidoUpdate, Partido, PartidoCreateDB
from app.utils.date_utils import parse_and_convert_to_utc
from sqlalchemy import asc

class CRUDPartido(CRUDBase[PartidoModel, PartidoCreateDB, PartidoUpdate]):
    def create(self, db: Session, *, obj_in: PartidoCreateDB) -> PartidoModel:
        db_obj = PartidoModel(
            fecha=obj_in.fecha,
            cancha=obj_in.cancha,
            horario_inicio_cancha=obj_in.horario_inicio_cancha,
            hora_local_actual=obj_in.hora_local_actual,
            horario=obj_in.horario,
            tipo_horario=obj_in.tipo_horario,
            round=obj_in.round,
            estado=obj_in.estado,
            hora_buenos_aires=obj_in.hora_buenos_aires,
            sets1=obj_in.sets1,
            sets2=obj_in.sets2,
            torneo_id=obj_in.torneo_id,
            equipo1_id=obj_in.equipo1_id,
            equipo2_id=obj_in.equipo2_id,
            es_despues_partido_anterior=obj_in.es_despues_partido_anterior
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_fecha_equipos(
        self, db: Session, *, fecha: str, cancha: str, round: str, equipo1_id: int, equipo2_id: int
    ) -> PartidoModel:
        return db.query(self.model).filter(
            self.model.fecha == fecha,
            self.model.cancha == cancha,
            self.model.round == round,
            ((self.model.equipo1_id == equipo1_id) & (self.model.equipo2_id == equipo2_id)) |
            ((self.model.equipo1_id == equipo2_id) & (self.model.equipo2_id == equipo1_id))
        ).first()

    def get_all(self, db: Session) -> List[Partido]:
        return db.query(Partido).options(
            joinedload(Partido.torneo),
            joinedload(Partido.equipo1).joinedload(Pareja.jugador1),
            joinedload(Partido.equipo1).joinedload(Pareja.jugador2),
            joinedload(Partido.equipo2).joinedload(Pareja.jugador1),
            joinedload(Partido.equipo2).joinedload(Pareja.jugador2)
        ).all()

    def update(
        self, db: Session, *, db_obj: Partido, obj_in: Union[PartidoUpdate, Dict[str, Any]]
    ) -> Partido:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete_all(self, db: Session) -> None:
        db.query(Partido).delete()
        db.commit()

    def get_by_torneo(self, db: Session, *, torneo_id: int) -> List[Partido]:
        return db.query(Partido).filter(Partido.torneo_id == torneo_id).options(
            joinedload(Partido.torneo),
            joinedload(Partido.equipo1).joinedload(Pareja.jugador1),
            joinedload(Partido.equipo1).joinedload(Pareja.jugador2),
            joinedload(Partido.equipo2).joinedload(Pareja.jugador1),
            joinedload(Partido.equipo2).joinedload(Pareja.jugador2)
        ).all()

    def get_by_torneo_and_fecha(self, db: Session, *, torneo_id: int, fecha: str) -> List[Partido]:
        return db.query(Partido).filter(Partido.torneo_id == torneo_id, Partido.fecha == fecha).all()

    def get_by_jugador(self, db: Session, *, jugador_id: int) -> List[Partido]:
        return db.query(Partido).join(Pareja, (Partido.equipo1_id == Pareja.id) | (Partido.equipo2_id == Pareja.id)) \
                            .filter((Pareja.jugador1_id == jugador_id) | (Pareja.jugador2_id == jugador_id)) \
                            .all()

    def get_by_torneo_and_round(self, db: Session, *, torneo_id: int, round_id: str) -> List[Partido]:
        return db.query(Partido).filter(Partido.torneo_id == torneo_id, Partido.round == round_id).all()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[PartidoModel]:
        return db.query(self.model).options(
            joinedload(self.model.equipo1).joinedload(Pareja.jugador1),
            joinedload(self.model.equipo1).joinedload(Pareja.jugador2),
            joinedload(self.model.equipo2).joinedload(Pareja.jugador1),
            joinedload(self.model.equipo2).joinedload(Pareja.jugador2),
            joinedload(self.model.torneo)
        ).order_by(asc(self.model.fecha), asc(self.model.horario_inicio_cancha)).offset(skip).limit(limit).all()

partido = CRUDPartido(PartidoModel)