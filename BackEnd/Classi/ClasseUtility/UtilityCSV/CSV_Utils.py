import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from Classi.ClasseMenu.Classe_t_menuServiziAssociazione.Domain_t_menuServiziAssociazione import TMenuServiziAssociazione
# Importa tutte le tue classi SQLAlchemy
from Classi.ClasseDB.db_connection import Base,  engine


def populate_from_csv_with_ids(session, classe, file_path):
    # Crea la tabella nel database se non esiste già
    Base.metadata.create_all(bind=engine)

    # Leggi il CSV
    df = pd.read_csv(file_path)

    # Verifica se ci sono dati già esistenti nella tabella
    inspector = inspect(engine)
    if inspector.has_table(classe.__tablename__):
        existing_ids = set(row.id for row in session.query(classe).all())
        df = df[~df['id'].isin(existing_ids)]

    if not df.empty:
        try:
            # Popola la tabella con i dati dal CSV
            df.to_sql(classe.__tablename__, con=engine, if_exists='append', index=False)
        except IntegrityError as e:
            print(f"Errore durante il popolamento delle tabelle: {e.orig}")
            session.rollback()
        else:
            session.commit()

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError

# Importa tutte le tue classi SQLAlchemy
from Classi.ClasseDB.db_connection import Base,  engine


def populate_from_csv_with_ids(session, classe, file_path):
    # Crea la tabella nel database se non esiste già
    Base.metadata.create_all(bind=engine)

    # Leggi il CSV
    df = pd.read_csv(file_path)

    # Verifica se ci sono dati già esistenti nella tabella
    inspector = inspect(engine)
    if inspector.has_table(classe.__tablename__):
        existing_ids = set(row.id for row in session.query(classe).all())
        df = df[~df['id'].isin(existing_ids)]

    if not df.empty:
        try:
            # Popola la tabella con i dati dal CSV
            df.to_sql(classe.__tablename__, con=engine, if_exists='append', index=False)
        except IntegrityError as e:
            print(f"Errore durante il popolamento delle tabelle: {e.orig}")
            session.rollback()
        else:
            session.commit()

