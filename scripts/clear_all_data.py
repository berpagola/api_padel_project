import sys
import os
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.partido import Partido
from app.models.jugador import Jugador
from app.models.pareja import Pareja
from app.models.torneo import Torneo
from app.core.config import settings

def clear_all_data():
    print(f"Intentando conectar a: {settings.DATABASE_URL}")
    db = SessionLocal()
    try:
        db.query(Partido).delete()
        db.query(Pareja).delete()
        db.query(Jugador).delete()
        db.query(Torneo).delete()
        db.commit()
        print("Todos los datos han sido eliminados")
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_data()