'''
session.py: Aquí se está configurando la conexión a la base de datos, 
utilizando SQLite en el archivo data.db, 
y una función get_db que proporcionará una sesión a las rutas de la API 
cuando sea necesario (usando FastAPI, por ejemplo).
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()