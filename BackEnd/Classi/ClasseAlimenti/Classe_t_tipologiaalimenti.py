from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from .Classe_t_tipologiaconservazione import TTipologiaConservazioni  # Assicurati che il percorso sia corretto

class TTipologiaAlimenti(Base):
    __tablename__ = 't_tipologiaalimenti'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descrizione = Column(String)
    conservazione_id = Column(Integer, ForeignKey('t_tipologiaconservazioni.ID'))
    conservazione = relationship('TTipologiaConservazioni', foreign_keys=[conservazione_id])

    def __repr__(self):
        return f"<TTipologiaAlimenti(nome='{self.nome}', descrizione='{self.descrizione}')>"