from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.sql import func
# from Classi.ClasseMenu.Classe_t_tipiMenu.Domain_t_tipiMenu import TTipiMenu
class TMenu(Base):
    __tablename__ = 't_menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=True)
    fkTipoMenu = Column(Integer, ForeignKey('t_tipimenu.id'), nullable=True)
    dataInserimento = Column(DateTime, nullable=True, default=func.now())
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    menu_servizi = relationship("TMenuServizi", back_populates="menu", uselist=True)
    tipi_menu = relationship("TTipiMenu", back_populates="menu", uselist=True)