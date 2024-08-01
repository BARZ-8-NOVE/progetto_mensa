from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TTipiAlimentazione(Base):
    __tablename__ = 't_tipialimentazione'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkTipoDieta = Column(Integer, ForeignKey('t_tipidiete.id'), nullable=True)
    descrizione = Column(String(50), nullable=True)
    note = Column(Text, nullable=True)
    ordinatore = Column(Integer, default=0, nullable=False)
    
    # Definizione della relazione con TTipiDiete
    tipo_dieta = relationship('TTipiDiete', backref='tipi_alimentazione')

  