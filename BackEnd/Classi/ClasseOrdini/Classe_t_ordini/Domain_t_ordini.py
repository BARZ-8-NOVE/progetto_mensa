from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class TOrdini(Base):
    __tablename__ = 't_ordinischede'

    id = Column(Integer, primary_key=True)
    fkReparto = Column(Integer, ForeignKey('t_reparti.id'), nullable=True)
    data = Column(Date, nullable=False)
    fkServizio = Column(Integer, ForeignKey('t_servizi.id'), nullable=True)
    cognome = Column(String(50))
    nome = Column(String(50))
    letto = Column(String(10))
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    # Definisci le relazioni dopo che le classi dipendenti sono state definite
    reparto = relationship("TReparti", back_populates="odrini")
    servizio = relationship("TServizi", back_populates="odrini")
