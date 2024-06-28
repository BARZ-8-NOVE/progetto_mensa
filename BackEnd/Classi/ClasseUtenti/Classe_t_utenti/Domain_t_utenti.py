from sqlalchemy import Column, String, Integer, ForeignKey, Index, Date
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Domain_t_tipiUtenti import TTipiUtenti

class TUtenti(Base):
    __tablename__ = 't_utenti'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    fkTipoUtente = Column(Integer, ForeignKey('t_tipiUtenti.id'), nullable=False)
    fkFunzCustom = Column(String, nullable=True)
    reparti = Column(String, nullable=True)
    attivo = Column(TINYINT, nullable=True)
    inizio = Column(Date, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullabla=False)

    tipoUtente = relationship('TTipiUtenti', foreign_keys=[fkTipoUtente])

    __table_args__ = (
        Index('idx_t_utenti', 'fkTipoUtente'),
        Index('idx_t_utenti', 'username'),
        Index('idx_t_utenti', 'email')
    )