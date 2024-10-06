from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base_class import Base

print(f"Creating engine with URL: {settings.DATABASE_URL}")
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Importa aquí todos tus modelos
from app.models.partido import Partido
from app.models.jugador import Jugador
from app.models.pareja import Pareja
from app.models.torneo import Torneo