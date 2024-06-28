from sqlalchemy import Column, Integer, String, DateTime
from Classi.ClasseDB.db_connection import Base

class TTipiMenu(Base):
    __tablename__ = 't_tipimenu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descrizione = Column(String(255), nullable=False)
    color = Column(String(50), nullable=True)
    backgroundColor = Column(String(50), nullable=True)
    ordinatore = Column(Integer, nullable=True)
    dataInserimento = Column(DateTime, nullable=True)
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)
