from sqlalchemy import Column, Integer, String
from Classi.ClasseDB.db_connection import Base

class TAllergeni(Base):
    __tablename__ = 't_allergeni'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)  
