from sqlalchemy import Column, String, Integer
from Classi.ClasseDB.db_connection import Base

class TAutorizzazioni(Base):
    __tablename__ = 't_autorizzazioni'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String, nullable=True)
    fkListaFunzionalita = Column(String, nullable=True)