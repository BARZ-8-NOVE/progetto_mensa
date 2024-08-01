from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URI

Base = declarative_base()
engine = create_engine(DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
metadata.bind = engine

def get_db():
    """Crea una nuova sessione di database per ogni richiesta."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

