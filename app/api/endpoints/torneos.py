from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.api import deps
from app.core.exceptions import TorneoNotFoundException, DatabaseOperationException

router = APIRouter()

@router.post("/", response_model=schemas.Torneo)
def create_or_update_torneo(
    torneo: schemas.TorneoCreate,
    db: Session = Depends(deps.get_db)
):
    try:
        return crud.torneo.create_or_update(db=db, obj_in=torneo)
    except Exception as e:
        raise DatabaseOperationException(str(e))

@router.get("/", response_model=List[schemas.Torneo])
def read_torneos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    torneos = crud.torneo.get_multi(db, skip=skip, limit=limit)
    return torneos

@router.get("/{torneo_id}", response_model=schemas.Torneo)
def read_torneo(
    torneo_id: int,
    db: Session = Depends(deps.get_db)
):
    torneo = crud.torneo.get(db, id=torneo_id)
    if torneo is None:
        raise TorneoNotFoundException(torneo_id)
    return torneo

# Puedes agregar más endpoints según sea necesario
