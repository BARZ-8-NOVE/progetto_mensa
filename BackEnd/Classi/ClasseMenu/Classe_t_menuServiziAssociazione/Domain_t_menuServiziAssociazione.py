from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.sql import func

class TMenuServiziAssociazione(Base):
    __tablename__ = 't_menuserviziassociazione'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkMenuServizio = Column(Integer, ForeignKey('t_menuservizi.id'), nullable=True)
    fkAssociazione = Column(Integer, ForeignKey('t_associazionepiattipreparazioni.id'), nullable=True)
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    menu_servizi = relationship("TMenuServizi", back_populates="menu_servizi_associazione")
    associazioni = relationship("TAssociazionePiattiPreparazioni", back_populates="menu_servizi_associazione", uselist=True) 

