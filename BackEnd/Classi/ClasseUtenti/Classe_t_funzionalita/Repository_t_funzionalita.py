from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita

class Repository_t_funzionalita:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_funzionalita_all(self):
        try:
            results = self.session.query(TFunzionalita).all()
        except Exception as e:
            return {'Error': str(e)}, 500
        return [{'id': result.id, 'nome': result.nome, 'frmNome': result.frmNome} for result in results]

    def get_funzionalita_by_id(self, id):
        try:
            result = self.session.query(TFunzionalita).filter_by(id=id).first()
        except Exception as e:
            return {'Error':str(e)}, 400
        if result:
            return {'id': result.id, 'nome': result.nome, 'frmNome': result.frmNome}
        else:
            return {'Error':f'No match found for this id: {id}'}, 404
        
    def create_funzionalita(self, id, nome, frmNome):
        try:
            funzionalita = TFunzionalita(id=id, nome=nome, frmNome = frmNome)
            self.session.add(funzionalita)
            self.session.commit()
            return {'Funzionalita':'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}
    
