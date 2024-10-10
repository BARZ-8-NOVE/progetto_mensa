from sqlalchemy import Column, Integer, String, Text, Date, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Classi.ClasseDB.db_connection import Base

class TSchedePreconfezionate(Base):
    __tablename__ = 't_schedepreconfezionate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkScheda = Column(Integer, ForeignKey('t_schede.id'), nullable=True)
    fkServizio = Column(Integer, ForeignKey('t_servizi.id'), nullable=True)
    descrizione = Column(String(100), nullable=True)
    note = Column(String(500), nullable=True)
    ordinatore = Column(Integer, default=0, nullable=False)
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime(timezone=True), nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    # Cambia il nome del backref per evitare conflitti
    scheda = relationship("TSchede", back_populates='schede_preconfezionate')
    servizi = relationship("TServizi", backref="schede_preconfezionate")