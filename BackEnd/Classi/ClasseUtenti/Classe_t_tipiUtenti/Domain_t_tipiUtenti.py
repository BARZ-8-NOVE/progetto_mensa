from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Domain_t_autorizzazioni import TAutorizzazioni

class TTipiUtenti(Base):
    __tablename__ = 't_tipiUtenti'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nomeTipoUtente = Column(String, nullable=True)
    fkAutorizzazioni = Column(Integer, ForeignKey('t_autorizzazioni.id'), nullable=True)

    autorizzazioni = relationship('TAutorizzazioni', foreign_keys=[fkAutorizzazioni])

    __table_args__ = (
        Index('idx_fk_autorizzazioni', 'fkAutorizzazioni'),
    )