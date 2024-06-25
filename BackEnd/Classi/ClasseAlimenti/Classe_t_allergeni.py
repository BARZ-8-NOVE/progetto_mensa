from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ClasseDB.config import DATABASE_URI

Base = declarative_base()

class TAllergeni(Base):
    __tablename__ = 't_allergeni'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)

    def __init__(self, db_session):
        self.db_session = db_session

    def get_t_allergeni_by_id(self, id):
        try:
            result = self.db_session.query(TAllergeni).filter_by(ID=id).first()
            if result:
                return {'id': result.ID,
                        'nome': result.nome}
            
            else:
                return {'Error': 'No data found for the given id'}, 404
        except Exception as e:
            return {'Error': str(e)}, 500

    def get_db_session():
        engine = create_engine(DATABASE_URI)
        Session = sessionmaker(bind=engine)
        return Session()