from sqlalchemy import Column, Integer, String
from Classi.ClasseDB.db_connection import Base

class TTipologiaConservazioni(Base):
    __tablename__ = 't_tipologiaconservazione'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)



