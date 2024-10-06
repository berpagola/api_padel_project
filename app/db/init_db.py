from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.base import engine
from app.models import partido, jugador, pareja, torneo  # Asegúrate de importar todos tus modelos

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada.")