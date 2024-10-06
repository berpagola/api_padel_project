import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models
from app.api import deps
from app.schemas.partido import Partido, PartidoList, PartidoCreate, PartidoUpdate, PartidoCreateDB
from app.crud.crud_pareja import pareja as crud_pareja
from app.core.exceptions import PartidoNotFoundException, DatabaseOperationException, ValidationException, TorneoNotFoundException, JugadorNotFoundException

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=List[Partido])
def create_partidos(
    partidos: PartidoList,
    db: Session = Depends(deps.get_db)
):
    logger.info(f"Received request to create {len(partidos.partidos)} partidos")
    created_or_updated_partidos = []
    for partido_data in partidos.partidos:
        try:
            # Verificar si el torneo existe
            torneo = crud.torneo.get(db, id=partido_data.torneo_id)
            if not torneo:
                logger.error(f"Torneo with id {partido_data.torneo_id} not found")
                raise HTTPException(status_code=404, detail=f"Torneo with id {partido_data.torneo_id} not found")

            # Procesar equipo1
            equipo1 = crud_pareja.create_with_jugadores(
                db, 
                jugador1=partido_data.equipo1.jugadores[0],
                jugador2=partido_data.equipo1.jugadores[1]
            )
            # Procesar equipo2
            equipo2 = crud_pareja.create_with_jugadores(
                db, 
                jugador1=partido_data.equipo2.jugadores[0],
                jugador2=partido_data.equipo2.jugadores[1]
            )
            
            logger.info(f"Searching for existing partido: fecha={partido_data.fecha}, cancha={partido_data.cancha}, round={partido_data.round}, equipo1_id={equipo1.id}, equipo2_id={equipo2.id}")
            
            # Buscar si el partido ya existe
            existing_partido = crud.partido.get_by_fecha_equipos(
                db, 
                fecha=partido_data.fecha,
                cancha=partido_data.cancha,
                round=partido_data.round,
                equipo1_id=equipo1.id,
                equipo2_id=equipo2.id
            )
            
            if existing_partido:
                logger.info(f"Existing partido found with id {existing_partido.id}")
                # Si el partido existe, actualizarlo
                partido_update = PartidoUpdate(**partido_data.dict(exclude={'equipo1', 'equipo2'}))
                partido_update.equipo1_id = equipo1.id
                partido_update.equipo2_id = equipo2.id
                updated_partido = crud.partido.update(db, db_obj=existing_partido, obj_in=partido_update)
                created_or_updated_partidos.append(updated_partido)
                logger.info(f"Updated existing partido for fecha {partido_data.fecha}")
            else:
                logger.info("No existing partido found, creating new one")
                # Si el partido no existe, crearlo
                partido_create_dict = partido_data.dict(exclude={'equipo1', 'equipo2'})
                partido_create_dict['equipo1_id'] = equipo1.id
                partido_create_dict['equipo2_id'] = equipo2.id
                logger.info(f"Creating new partido with data: {partido_create_dict}")
                partido_create = PartidoCreateDB(**partido_create_dict)
                new_partido = crud.partido.create(db, obj_in=partido_create)
                created_or_updated_partidos.append(new_partido)
                logger.info(f"Created new partido for fecha {partido_data.fecha}")
            
        except HTTPException as he:
            logger.error(f"HTTP error processing partido: {str(he)}")
            raise he
        except Exception as e:
            logger.error(f"Error processing partido: {str(e)}")
            db.rollback()  # Rollback the transaction in case of error
            raise HTTPException(status_code=500, detail=f"Error processing partido: {str(e)}")
    
    db.commit()  # Commit all changes at the end
    logger.info(f"Successfully created/updated {len(created_or_updated_partidos)} partidos")
    return created_or_updated_partidos

@router.get("/", response_model=List[Partido])
def read_partidos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    print("Endpoint GET /partidos/ llamado")
    try:
        partidos = crud.partido.get_multi(db, skip=skip, limit=limit)
        return partidos
    except Exception as e:
        print(f"Error en read_partidos: {str(e)}")
        raise DatabaseOperationException(str(e))

@router.get("/raw", response_model=None)
def read_partidos_raw(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    print("Endpoint GET /partidos/raw llamado")
    try:
        partidos = crud.partido.get_multi(db, skip=skip, limit=limit)
        return [{"id": p.id, "fecha": p.fecha} for p in partidos]
    except Exception as e:
        print(f"Error en read_partidos_raw: {str(e)}")
        raise DatabaseOperationException(str(e))

# Actualiza los otros endpoints de manera similar