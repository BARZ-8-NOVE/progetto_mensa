from sqlalchemy import Column, String, Integer, ForeignKey, Index, Date, UniqueConstraint
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Domain_t_tipiUtenti import TTipiUtenti

class TUtenti(Base):
    __tablename__ = 't_utenti'

    id = Column(Integer, autoincrement=True, primary_key=True)
    public_id = Column(String, nullable=True, unique=True)
    username = Column(String, nullable=False, unique=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    fkTipoUtente = Column(Integer, ForeignKey('t_tipiUtenti.id'), nullable=False)
    fkFunzCustom = Column(String, nullable=True)
    reparti = Column(String, nullable=True)
    attivo = Column(TINYINT, nullable=True)
    inizio = Column(Date, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    tipoUtente = relationship('TTipiUtenti', foreign_keys=[fkTipoUtente])
    # utente_log = relationship('TUserActivityLog', back_populates= 'utente')

    __table_args__ = (
        Index('fkTipoUtente', 'fkTipoUtente'),
        UniqueConstraint('username', 'username'),
        UniqueConstraint('email', 'email'),
        UniqueConstraint('public_id', 'public_id')
    )