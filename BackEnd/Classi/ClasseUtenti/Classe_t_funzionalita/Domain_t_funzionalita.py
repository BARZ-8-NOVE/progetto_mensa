from sqlalchemy import Column, Integer, String, DateTime, Boolean
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.orm import relationship

class TFunzionalita(Base):
    __tablename__ = 't_funzionalita'

    id = Column(Integer, primary_key=True, autoincrement=True)
    menuPrincipale = Column(Boolean, default=False)
    fkPadre= Column(Integer, nullable=True)
    titolo = Column(String(100), nullable=True)
    label = Column(String(100), nullable=True)
    icon = Column(String(100), nullable=True)
    link = Column(String(100), nullable=True)
    ordinatore = Column(Integer, nullable=False)
    target = Column(String(15), nullable=False)
    dataCancellazione = Column(DateTime, nullable=True)

    funzionalita_utente = relationship("TFunzionalitaUtente", back_populates="funzionalita")