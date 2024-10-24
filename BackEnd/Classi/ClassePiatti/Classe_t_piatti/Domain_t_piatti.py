from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.sql import func


class TPiatti(Base):
    __tablename__ = 't_piatti'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkTipoPiatto = Column(Integer, ForeignKey('t_tipipiatti.id'), nullable=True)
    codice = Column(String(15), nullable=True)
    titolo = Column(String(50), nullable=True)
    descrizione = Column(String(100), nullable=True)
    inMenu = Column(Boolean, nullable=False, default=False)
    ordinatore = Column(Integer, nullable=False, default=0)
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    # Definizione delle relazioni
    tipo_piatto = relationship("TTipiPiatti", back_populates="piatti")
    schede_piatti = relationship('TSchedePiatti', back_populates='piatto')