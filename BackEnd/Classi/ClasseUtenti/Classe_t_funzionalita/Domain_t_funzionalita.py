from sqlalchemy import Column, String, Integer
from Classi.ClasseDB.db_connection import Base

class TFunzionalita(Base):
    __tablename__ = 't_funzionalita'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String, nullable=True)
    frmNome = Column(String, nullable=True)