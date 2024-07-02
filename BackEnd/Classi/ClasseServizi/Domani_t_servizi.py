from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TServizi(Base):
    __tablename__ = 't_servizi'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descrizione = Column(String(30))
    ordinatore = Column(Integer)
    inMenu = Column(Boolean)

    # Definizione della relazione inversa
    piatti = relationship("TPiatti", back_populates="servizio")
    menu_servizi = relationship("TMenuServizi", back_populates="servizio")