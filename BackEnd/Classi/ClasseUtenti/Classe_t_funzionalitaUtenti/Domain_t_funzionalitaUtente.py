from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TFunzionalitaUtente(Base):
    __tablename__ = 't_funzionalitaUtente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkTipoUtente = Column(Integer, ForeignKey('t_tipiUtenti.id'))
    fkFunzionalita = Column(Integer, ForeignKey('t_funzionalita.id'))
    permessi = Column(Boolean, default=True)

    # Establishing relationships with explicit foreign_keys
    tipiUtente = relationship("TTipiUtenti", foreign_keys=[fkTipoUtente])
    funzionalita = relationship("TFunzionalita", foreign_keys=[fkFunzionalita])
