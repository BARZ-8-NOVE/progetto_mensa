from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.sql import func

class TMenuServizi(Base):
    __tablename__ = 't_menuservizi'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkMenu = Column(Integer, ForeignKey('t_menu.id'), nullable=True)
    fkServizio = Column(Integer, ForeignKey('t_servizi.id'), nullable=True)
    note = Column(Text, nullable=True)
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    menu = relationship("TMenu", back_populates="menu_servizi")
    
    servizio = relationship("TServizi", back_populates="menu_servizi")