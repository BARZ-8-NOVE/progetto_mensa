from sqlalchemy import Column, Integer, String
from Classi.ClasseDB.db_connection import Base

class TOrdiniPiatti(Base):
    __tablename__ = 't_ordinipiatti'