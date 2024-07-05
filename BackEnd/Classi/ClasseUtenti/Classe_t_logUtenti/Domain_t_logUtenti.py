from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.sql import func

class TUserActivityLog(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    fkUtente = Column(Integer, ForeignKey('t_utenti.id'), nullable=False)
    azione = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=True, default=func.now())
    dettagli = Column(String(4000))

utente = relationship ('TUtenti', back_populates= 'utente_log') 
