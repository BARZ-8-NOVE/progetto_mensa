from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ClasseDB.config import DATABASE_URI

# Creazione dell'engine SQLAlchemy
engine = create_engine(DATABASE_URI)

# Creazione di una session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Crea una nuova sessione di database per ogni richiesta."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
