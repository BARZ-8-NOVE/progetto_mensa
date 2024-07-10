from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base


class TFrontEndVociFiglieMenu(Base):
    __tablename__ = 't_frontEndVociFiglieMenu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkidFrontEndVociMenu = Column(Integer, ForeignKey('t_frontEndVociMenu.id'))
    titolo = Column(String(100), nullable=True)
    label = Column(String(100), nullable=True)
    icon = Column(String(100), nullable=True)
    link = Column(String(100), nullable=True)
    ordinatore = Column(Integer, nullable=False)
    target = Column(String(15), nullable=False)
    dataCancellazione = Column(DateTime, nullable=True)

    voci_menu_figlie = relationship("TFrontEndVociMenu", foreign_keys=[fkidFrontEndVociMenu])