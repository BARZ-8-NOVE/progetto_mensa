from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base


class TTipologiaAlimenti(Base):
    __tablename__ = 't_tipologiaalimenti'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)  
    fktipologiaConservazione = Column(Integer, ForeignKey('t_tipologiaconservazione.id'))

    # Correct the spelling here
    alimenti = relationship('TAlimenti', back_populates='tipologia')

