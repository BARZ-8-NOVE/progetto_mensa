from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseAlimenti.Classe_t_allergeni.Domani_t_allergeni import TAllergeni
from Classi.ClasseAlimenti.Classe_t_tipologiaalimenti.Domani_t_tipologiaalimenti import TTipologiaAlimenti

class TAlimenti(Base):
    __tablename__ = 't_alimenti_con_allergeni'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Alimento = Column(String, nullable=False)
    Energia_Kcal = Column(Float)
    Energia_KJ = Column(Float)
    Prot_Tot_Gr = Column(Float)
    Glucidi_Tot = Column(Float)
    Lipidi_Tot = Column(Float)
    Saturi_Tot = Column(Float)
    fkAllergene = Column(Integer, ForeignKey('t_allergeni.id'))
    fkTipologiaAlimento = Column(Integer, ForeignKey('t_tipologiaalimenti.id'))

    # Definizioni delle relazioni

    tipologia_alimento = relationship("TTipologiaAlimenti", foreign_keys=[fkTipologiaAlimento])
    
