from sqlalchemy import Column, Integer, String
from Classi.ClasseDB.db_connection import Base

class TAllergeni(Base):
    __tablename__ = 't_allergeni'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)

    def get_t_allergeni_by_id(self, db_session, id):
        try:
            result = db_session.query(TAllergeni).filter_by(ID=id).first()
            if result:
                return {'id': result.ID, 'nome': result.nome}
            else:
                return {'Error': 'No data found for the given id'}, 404
        except Exception as e:
            return {'Error': str(e)}, 500