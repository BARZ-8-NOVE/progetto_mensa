from sqlalchemy import Column, Integer, String, ForeignKey
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.orm import relationship

class TTipologiaConservazioni(Base):
    __tablename__ = 't_tipologiaconservazioni'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)


