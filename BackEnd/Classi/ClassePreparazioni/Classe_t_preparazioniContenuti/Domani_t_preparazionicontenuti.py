from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Classi.ClasseDB.db_connection import Base

class TPreparazioniContenuti(Base):
    __tablename__ = 't_preparazionicontenuti'

    id = Column(Integer, primary_key=True)
    fkPreparazione = Column(Integer, nullable=False)
    fkAlimento = Column(Integer, nullable=True)
    quantita = Column(Float, nullable=False)
    fkTipoQuantita = Column(Integer, ForeignKey('t_tipoquantita.id'), nullable=False)
    note = Column(String(255), nullable=True)
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)


    tipo_quantita = relationship("TTipoQuantita", back_populates="contenuti")