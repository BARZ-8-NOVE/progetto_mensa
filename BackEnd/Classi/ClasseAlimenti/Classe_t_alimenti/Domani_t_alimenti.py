from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base


class TAlimenti(Base):
    __tablename__ = 't_alimenti_con_allergeni'

    id = Column(Integer, primary_key=True, autoincrement=True)
    alimento = Column(String(255), nullable=False)
    energia_Kcal = Column(Float)
    energia_KJ = Column(Float)
    prot_tot_gr = Column(Float)
    glucidi_tot = Column(Float)
    lipidi_tot = Column(Float)
    saturi_tot = Column(Float)
    fkAllergene = Column(String(255))
    fkTipologiaAlimento = Column(Integer, ForeignKey('t_tipologiaalimenti.id'))

    # Definizioni delle relazioni

    tipologia_alimento = relationship("TTipologiaAlimenti", foreign_keys=[fkTipologiaAlimento])


