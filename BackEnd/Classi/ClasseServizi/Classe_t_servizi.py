from sqlalchemy import Column, Integer, String, Boolean
from Classi.ClasseDB.db_connection import Base

class TServizi(Base):
    __tablename__ = 't_servizi'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descrizione = Column(String(30))
    ordinatore = Column(Integer)
    inMenu = Column(Boolean)

    def __repr__(self):
        return f"<TServizi(id={self.id}, descrizione='{self.descrizione}', ordinatore={self.ordinatore}, inMenu={self.inMenu})>"
