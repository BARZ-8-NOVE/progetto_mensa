from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
# from Classi.ClasseOrdini.Classe_t_ordini.Domain_t_ordini import TOrdini
# from Classi.ClasseMenu.Classe_t_menuServizi.Domain_t_menuServizi import TMenuServizi
class TServizi(Base):
    __tablename__ = 't_servizi'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descrizione = Column(String(30))
    ordinatore = Column(Integer)
    inMenu = Column(TINYINT, nullable=True)

    # Relazione con TMenuServizi
    menu_servizi = relationship("TMenuServizi", back_populates="servizio")

    ordini = relationship("TOrdini", back_populates="servizio")