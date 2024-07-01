from sqlalchemy import Column, Integer, String, Float
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.orm import relationship

class TTipoQuantita(Base):
    __tablename__ = 't_tipoquantita'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(255), nullable=False)
    peso_valore_in_grammi = Column(Float ,nullable=True)
    peso_valore_in_Kg = Column(Float ,nullable=True)

    contenuti = relationship("TPreparazioniContenuti", back_populates="tipo_quantita")