import sys
import os
from dotenv import load_dotenv

# Añade el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Carga manualmente las variables de entorno
load_dotenv(os.path.join(project_root, '.env'))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.partido import Partido
from app.core.config import settings

def clear_partidos():
    print(f"Intentando conectar a: {settings.DATABASE_URL}")
    db = SessionLocal()
    try:
        db.query(Partido).delete()
        db.commit()
        print("Todos los partidos han sido eliminados")
    finally:
        db.close()

if __name__ == "__main__":
    clear_partidos()