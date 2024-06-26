from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ClasseDB.db_connection import Base

class TTipologiaAlimenti(Base):
    __tablename__ = 't_tipologiaalimenti'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    fktipologiaConservazione = Column(Integer, ForeignKey('t_tipologiaconservazione.ID'))

    # Definizione della relazione con TTipologiaConservazioni
    tipologia_conservazione = relationship("TTipologiaConservazioni")

    def get_t_tipologiaAlimenti_by_id(self, db_session, id):
        try:
            result = db_session.query(TTipologiaAlimenti).filter_by(ID=id).first()
            if result:
                return {
                    'id': result.ID,
                    'nome': result.nome,
                    'fktipologiaConservazione': result.fktipologiaConservazione
                }
            else:
                return {'Error': 'No data found for the given id'}, 404
        except Exception as e:
            return {'Error': str(e)}, 500
