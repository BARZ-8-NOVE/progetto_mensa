from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TReparti(Base):
    __tablename__ = 't_reparti'

    id = Column(Integer, primary_key=True)
    codiceAreas = Column(String(10), nullable=True)
    descrizione = Column(String(100), nullable=True)
    sezione = Column(String(50), nullable=True)
    ordinatore = Column(int, nullable=False)
    padiglione = Column(String(50), nullable=True)
    piano = Column(String(50), nullable=True)
    lato = Column(String(50), nullable=True)
    inizio = Column(DateTime, nullable=True)
    fine = Column(DateTime, nullable=True)
    dataInserimento = Column(DateTime, nullable=True)
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)
