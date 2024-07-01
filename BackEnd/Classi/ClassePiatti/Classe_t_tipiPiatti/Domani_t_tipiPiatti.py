from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Classi.ClasseDB.db_connection import Base

class TTipiPiatti(Base):
    __tablename__ = 't_tipipiatti'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descrizione = Column(String(50), nullable=True)
    descrizionePlurale = Column(String(50), nullable=True)
    inMenu = Column(Boolean, nullable=False, default=False)
    ordinatore = Column(Integer, nullable=False, default=0)
    color = Column(String(7), nullable=True)
    backgroundColor = Column(String(7), nullable=True)
    dataInserimento = Column(DateTime, nullable=False, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    # Definizione delle relazioni
    piatti = relationship("TPiatti", back_populates="tipo_piatto")
