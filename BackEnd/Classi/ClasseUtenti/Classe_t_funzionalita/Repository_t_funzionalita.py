from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita

class Repository_t_funzionalita:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_funzionalita(self, id:int):
        try:
            result = self.session.query(TFunzionalita).filter_by(id=id).first()
        except Exception as e:
            return {'Error':str(e)}, 400
        if result:
            return result
        else:
            return False

    def get_funzionalita_all(self):
        try:
            results = self.session.query(TFunzionalita).all()
            self.session.close()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500
        return [{'id': result.id, 'nome': result.nome, 'frmNome': result.frmNome} for result in results]

    def get_funzionalita_by_id(self, id:int):
        try:
            result = self.session.query(TFunzionalita).filter_by(id=id).first()
        except Exception as e:
            return {'Error':str(e)}, 400
        if result:
            self.session.close()
            return {'id': result.id, 'nome': result.nome, 'frmNome': result.frmNome}
        else:
            self.session.close()
            return {'Error':f'No match found for this id: {id}'}, 404
        
    def create_funzionalita(self, nome:str, frmNome:str):
        try:
            funzionalita = TFunzionalita(nome=nome, frmNome = frmNome)
            self.session.add(funzionalita)
            self.session.commit()
            self.session.close()
            return {'Funzionalita':'added!'}, 200
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}
        
    def update_funzionalita(self, id:int, nome:str, frmNome:str):
        try:
            result = self.exists_funzionalita(id)
            if result:
                result.nome = nome
                result.frmNome = frmNome
                self.session.commit()
                self.session.close()
                return {'Funzionalita':f'updated funzionalita for this id: {id}, nome: {nome}, frmNome: {frmNome}'}, 200
            else:
                self.session.rollback()
                self.session.close()
                return {'Error':f'no match found for this id: {id}'}, 403
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500
        
    def delete_funzionalita(self, id:int):
        try:
            result = self.exists_funzionalita(id)
            if result:
                self.session.delete(result)
                self.session.commit()
                self.session.close()
                return {'Funzionalita':f'deleted funzionalita for this id: {id}'}
            else:
                self.session.rollback()
                self.session.close()
                return {'Error':f'no match found for this id: {id}'}, 403
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500

    
