from sqlalchemy import Column, Integer, String
from Classi.ClasseDB.db_connection import Base, 

class TTipologiaConservazioni(Base):
    __tablename__ = 't_tipologiaconservazione'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)



# Creare una sessione
session = SessionLocal()

# Popolare la tabella
populate_from_csv_with_ids(session, TTipologiaConservazioni, 'DBMS/file_dati_statici/t_tipologiaconservazioni.csv')

# Chiudere la sessione
session.close()