from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.sql import func

class TSchedePiatti(Base):
    __tablename__ = 't_schedepiatti'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkScheda = Column(Integer, ForeignKey('t_schede.id'), nullable=True)
    fkServizio = Column(Integer, ForeignKey('t_servizi.id'), nullable=True)
    fkPiatto = Column(Integer, ForeignKey('t_piatti.id'), nullable=True)
    colonna = Column(Integer, default=0, nullable=False)
    riga = Column(Integer, default=0, nullable=False)
    note = Column(String(50), nullable=True)
    ordinatore = Column(Integer, default=0, nullable=False)
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime(timezone=True), nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    # Definizione delle relazioni
    scheda = relationship('TSchede', back_populates='schede_piatti')
    servizi = relationship('TServizi', back_populates='schede_piatti')
    piatto = relationship('TPiatti', back_populates='schede_piatti')


