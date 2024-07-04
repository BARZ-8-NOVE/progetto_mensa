from sqlalchemy import Column, Integer, String
from Classi.ClasseDB.db_connection import Base

class TTipologiaConservazioni(Base):
    __tablename__ = 't_tipologiaconservazione'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)  # Specifica la lunghezza di 255 per VARCHAR
    # Altri campi della tabella




