from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TPreparazioni(Base):
    __tablename__ = 't_preparazioni'

    id = Column(Integer, primary_key=True)
    fkTipoPreparazione = Column(Integer, ForeignKey('t_tipipreparazioni.id'), nullable=False)
    descrizione = Column(String(100), nullable=False)
    isEstivo = Column(Boolean, nullable=False)
    isInvernale = Column(Boolean, nullable=False)
    allergeni = Column(String(4000), nullable=True)
    inizio = Column(Date, nullable=True)
    fine = Column(Date, nullable=True)
    dataInserimento = Column(DateTime, nullable=True)
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)
    immagine = Column(String, nullable=True)  # varchar(MAX) viene trattato come una stringa di lunghezza variabile

    tipo_preparazione = relationship('TTipiPreparazioni')

