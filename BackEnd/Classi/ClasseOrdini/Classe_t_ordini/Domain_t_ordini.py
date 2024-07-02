from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class TOrdini(Base):
    __tablename__ = 't_ordini'

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    fkServizio = Column(Integer, nullable=False)
    note = Column(String)
    fkReparto = Column(Integer)
    cognome = Column(String(50))
    nome = Column(String(50))
    letto = Column(String(10))
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)
