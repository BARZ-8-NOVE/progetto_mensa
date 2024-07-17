from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# from Classi.ClasseServizi.Domani_t_servizi import TServizi
# from Classi.ClasseReparti.Domain_t_reparti import TReparti

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

    ordini_piatti = relationship("TOrdiniPiatti", back_populates="ordini", uselist=True)
    reparti = relationship("TReparti", back_populates="ordini", uselist=False)
    servizi = relationship("TServizi", back_populates="ordini", uselist=False)
