from sqlalchemy import Column, Integer, String, DateTime
from Classi.ClasseDB.db_connection import Base


class TFrontEndMenu(Base):
    __tablename__ = 't_frontEndMenu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titolo = Column(String(100), nullable=True)
    label = Column(String(100), nullable=True)
    icon = Column(String(100), nullable=True)
    link = Column(String(100), nullable=True)
    ordinatore = Column(Integer, nullable=False)
    target = Column(String(15), nullable=False)
    dataCancellazione = Column(DateTime, nullable=True)
