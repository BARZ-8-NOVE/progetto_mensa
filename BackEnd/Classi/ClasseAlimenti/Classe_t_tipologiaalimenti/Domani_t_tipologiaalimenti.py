from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from ..Classe_t_tipologiaconservazione.Domani_t_tipologiaconservazione import TTipologiaConservazioni

class TTipologiaAlimenti(Base):
    __tablename__ = 't_tipologiaalimenti'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    fktipologiaConservazione = Column(Integer, ForeignKey('t_tipologiaconservazioni.ID'))

    
