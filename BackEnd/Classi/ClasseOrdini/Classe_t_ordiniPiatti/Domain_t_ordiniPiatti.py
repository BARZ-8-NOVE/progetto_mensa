from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base


class TOrdiniPiatti(Base):
    __tablename__ = 't_ordinischedepiatti'

    id = Column(Integer, primary_key=True)
    fkOrdineScheda = Column(Integer, ForeignKey('t_ordinischede.id'))
    fkPiatto = Column(Integer, ForeignKey('t_piatti.id'))
    quantita = Column(Integer)
    note = Column(String(255))

    ordine_scheda = relationship("TOrdiniSchede", back_populates="ordini_piatti")
    piatto = relationship("TPiatti", back_populates="ordini_piatti")
