from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ClasseDB.db_connection import Base

class TAlimenti(Base):
    __tablename__ = 't_alimenti_con_allergeni'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Alimento = Column(String)
    Energia_Kcal = Column(Float)
    Energia_KJ = Column(Float)
    Prot_Tot_Gr = Column(Float)
    Glucidi_Tot = Column(Float)
    Glucidi_Solub = Column(Float)
    Lipidi_Tot = Column(Float)
    Saturi_Tot = Column(Float)
    fkAllergene = Column(Integer, ForeignKey('t_allergeni.id'))
    fkTipologiaAlimento = Column(Integer, ForeignKey('t_tipologiaalimenti.id'))

    # Definizioni delle relazioni
    allergene = relationship("TAllergeni")
    tipologia_alimento = relationship("TTipologiaAlimenti")

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
