from sqlalchemy import Column, Integer, String, DateTime
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class TTipiMenu(Base):
    __tablename__ = 't_tipimenu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descrizione = Column(String(255), nullable=False)
    color = Column(String(50), nullable=True)
    backgroundColor = Column(String(50), nullable=True)
    ordinatore = Column(Integer, nullable=True)
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    menu = relationship("TMenu", back_populates="tipi_menu",uselist=True)
    schede = relationship("TSchede", back_populates="tipi_menu",uselist=True)