from sqlalchemy import Column, Integer, String
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.orm import relationship

class TTipologiaConservazioni(Base):
    __tablename__ = 't_tipologiaconservazione'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)



