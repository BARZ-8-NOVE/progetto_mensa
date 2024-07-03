from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.sql import func

class TAssociazionePiattiPreparazioni(Base):
    __tablename__ = 't_associazionepiattipreparazioni'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkPiatto = Column(Integer, ForeignKey('t_piatti.id'), nullable=True)
    fkPreparazione = Column(Integer, ForeignKey('t_preparazioni.id'), nullable=True)
    dataInserimento = Column(DateTime, default=func.now(), nullable=True)
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    piatto = relationship("TPiatti", backref="associazioni")
    preparazione = relationship("TPreparazioni", backref="associazioni")
    ordini_piatti = relationship("TOrdiniPiatti", back_populates="associazioni")

    # ordini_piatti = relationship("TOrdiniPiatti", backref="associazioni")
