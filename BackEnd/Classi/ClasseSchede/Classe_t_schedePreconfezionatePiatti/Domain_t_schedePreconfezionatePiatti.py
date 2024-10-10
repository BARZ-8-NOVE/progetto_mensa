from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Classi.ClasseDB.db_connection import Base

class TSchedePreconfezionatePiatti(Base):
    __tablename__ = 't_schedePreconfezionatePiatti'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkSchedaPreconfezionata = Column(Integer, ForeignKey('t_schedepreconfezionate.id'), nullable=True)
    fkPiatto = Column(Integer, ForeignKey('t_piatti.id'), nullable=True)
    quantita = Column(Integer, nullable=True)
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime(timezone=True), nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)
    #Relazioni

    scheda_preconfezionata_piatti = relationship("TSchedePreconfezionate", backref="SchedaPreconfezionata")
    piatto = relationship("TPiatti", backref="piatti")

