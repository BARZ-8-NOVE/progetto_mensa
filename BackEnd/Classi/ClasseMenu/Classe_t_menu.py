from sqlalchemy import Column, Integer, String, Date, DateTime
from Classi.ClasseDB.db_connection import Base

class TMenu(Base):
    __tablename__ = 't_menu'

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    fkTipoMenu = Column(Integer, nullable=False)
    dataInserimento = Column(DateTime, nullable=True)
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)
