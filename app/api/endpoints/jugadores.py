from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Jugador])
def read_jugadores(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    jugadores = crud.jugador.get_multi(db, skip=skip, limit=limit)
    return jugadores

# Aquí puedes agregar más endpoints relacionados con jugadores
