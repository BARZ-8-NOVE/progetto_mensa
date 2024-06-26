from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from .Classe_t_allergeni import TAllergeni 
from .Classe_t_tipologiaalimenti import TTipologiaAlimenti

class TAlimenti(Base):
    __tablename__ = 't_alimenti_con_allergeni'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Alimento = Column(String)
    Energia_Kcal = Column(Float)
    Energia_KJ = Column(Float)
    Prot_Tot_Gr = Column(Float)
    Glucidi_Tot = Column(Float)
    Lipidi_Tot = Column(Float)
    Saturi_Tot = Column(Float)
    fkAllergene = Column(Integer, ForeignKey('t_allergeni.ID'))
    fkTipologiaAlimento = Column(Integer, ForeignKey('t_tipologiaalimenti.id'))

    # Definizioni delle relazioni
    allergene = relationship("TAllergeni", foreign_keys=[fkAllergene])
    tipologia_alimento = relationship("TTipologiaAlimenti", foreign_keys=[fkTipologiaAlimento])

    def get_t_alimenti_by_id(self, db_session, id):
        try:
            result = db_session.query(TAlimenti).filter_by(ID=id).first()
            if result:
                return {
                    'id': result.ID,
                    'alimento': result.Alimento,
                    'energia_kcal': result.Energia_Kcal,
                    'Energia_KJ': result.Energia_KJ,
                    'prot_tot_gr': result.Prot_Tot_Gr,
                    'glucidi_tot': result.Glucidi_Tot,
                    'lipidi_tot': result.Lipidi_Tot,
                    'saturi_tot': result.Saturi_Tot,
                    'fkAllergene': result.fkAllergene,
                    'fkTipologiaAlimento': result.fkTipologiaAlimento
                }
            else:
                return {'Error': 'No data found for the given id'}, 404
        except Exception as e:
            return {'Error': str(e)}, 500
        
        
    @classmethod
    def get_all(cls, db_session):
        try:
            results = db_session.query(cls).all()
            return [{
                'id': result.ID,
                'alimento': result.Alimento,
                'energia_kcal': result.Energia_Kcal,
                'energia_kj': result.Energia_KJ,
                'prot_tot_gr': result.Prot_Tot_Gr,
                'glucidi_tot': result.Glucidi_Tot,
                'lipidi_tot': result.Lipidi_Tot,
                'saturi_tot': result.Saturi_Tot,
                'fkAllergene': result.fkAllergene,
                'fkTipologiaAlimento': result.fkTipologiaAlimento
            } for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500