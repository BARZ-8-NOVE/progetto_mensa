from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Domain_t_associazionePiattiPreparazioni import TAssociazionePiattiPreparazioni
from Classi.ClasseDB.db_connection import Base


class TOrdiniPiatti(Base):
    __tablename__ = 't_ordinischedepiatti'

    id = Column(Integer, primary_key=True)
    fkOrdineScheda = Column(Integer, ForeignKey('t_ordinischede.id'))
    fkPiatto = Column(Integer, ForeignKey('t_associazionepiattipreparazioni.id'))
    quantita = Column(Integer)
    note = Column(String(255))

    ordiniSchede = relationship("TOrdiniSchede", back_populates="ordini_piatti")
    associazioni = relationship("TAssociazionePiattiPreparazioni", back_populates="ordini_piatti", uselist=False)
