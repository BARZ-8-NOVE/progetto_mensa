from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TTipiDiete(Base):
    __tablename__ = 't_tipidiete'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descrizione = Column(String(50), nullable=True)
    note = Column(Text, nullable=True)


    tipi_alimentazione = relationship('TTipiAlimentazione', back_populates='tipi_dieta')
