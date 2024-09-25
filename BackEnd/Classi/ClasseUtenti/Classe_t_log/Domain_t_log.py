from sqlalchemy import Column, String, Integer, JSON, DateTime, func
from Classi.ClasseDB.db_connection import Base

class TLog(Base):
    __tablename__ = 't_log'
    
    id = Column(Integer, primary_key=True)
    level = Column(String(50), nullable=False)  # Livello del log (INFO, WARNING, ERROR, etc.)
    message = Column(String(255), nullable=False)  # Messaggio del log
    timestamp = Column(DateTime, nullable=False, default=func.now())  # Quando è avvenuto il log
    fkUser = Column(String(50), nullable=False)   # ID dell'utente (se applicabile)
    route = Column(String(255), nullable=True)  # Il percorso della richiesta (opzionale)
    data = Column(JSON, nullable=True)  # Campo per ulteriori dati dell'operazione
