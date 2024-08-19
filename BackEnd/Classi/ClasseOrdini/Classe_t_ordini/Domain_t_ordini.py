
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base


class TOrdini(Base):
    __tablename__ = 't_ordini'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=True)
    fkServizio = Column(Integer, ForeignKey('t_servizi.id'), nullable=True)
    
    # Assuming there's a relationship with another table, e.g., TServizi
    servizi = relationship("TServizi", backref="ordine")
    # ordiniSchede = relationship("TOrdiniSchede", back_populates="ordine")