from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from sqlalchemy.sql import func

class TAssociazioneTipiPiattiTipiPreparazioni(Base):
    __tablename__ = 't_associazionetipipiattitipipreparazioni'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkTipoPiatto = Column(Integer, ForeignKey('t_tipipiatti.id'), nullable=False)
    fkTipoPreparazione = Column(Integer, ForeignKey('t_tipipreparazioni.id'), nullable=False)
    dataInserimento = Column(DateTime, default=func.now(), nullable=True)
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime, nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)

    # Relazioni con i modelli correlati
    tipo_piatto = relationship("TTipiPiatti", backref="associazioni_piatto")
    tipo_preparazione = relationship("TTipiPreparazioni", backref="associazioni_preparazione")
