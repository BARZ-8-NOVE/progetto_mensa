from sqlalchemy import Column, Integer, String
from Classi.ClasseDB.db_connection import Base

class TTipiPreparazioni(Base):
    __tablename__ = 't_tipipreparazioni'

    id = Column(Integer, primary_key=True)
    descrizione = Column(String(255), nullable=False)


