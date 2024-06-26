from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TTipiPreparazioniContenuti(Base):
    __tablename__ = 't_tipipreparazionicontenuti'

    id = Column(Integer, primary_key=True)
    fkPreparazione = Column(Integer, nullable=False)
    fkAlimento = Column(Integer, nullable=False)
    quantita = Column(Float, nullable=False)
    fkTipoQuantita = Column(Integer, ForeignKey('t_tipoquantita.id'), nullable=False)
    note = Column(String(255), nullable=True)
    dataInserimento = Column(DateTime, nullable=True)
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)


    tipo_quantita = relationship("TTipoQuantita", back_populates="contenuti")