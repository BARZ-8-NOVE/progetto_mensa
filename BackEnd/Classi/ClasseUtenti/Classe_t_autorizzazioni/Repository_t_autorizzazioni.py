from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Domain_t_autorizzazioni import TAutorizzazioni

class Repository_t_autorizzazioni:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_autorizzazione(self, id:int):
        try:
            result = self.session.query(TAutorizzazioni).filter_by(id=id).first()
        except Exception as e:
            return {'Error':str(e)}, 400
        if result:
            return result
        else:
            return False

    def get_autorizzazioni_all(self):
        try:
            results = self.session.query(TAutorizzazioni).all()
            self.session.close()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500
        return [{
                    'id': result.id,
                    'nome': result.nome, 
                    'fkListaFunzionalita': result.fkListaFunzionalita
                } for result in results]

    def get_autorizzazione_by_id(self, id:int):
        try:
            result = self.session.query(TAutorizzazioni).filter_by(id=id).first()
        except Exception as e:
            return {'Error':str(e)}, 400
        if result:
            self.session.close()
            return {'id': result.id, 'nome': result.nome, 'fkListaFunzionalita': result.fkListaFunzionalita}
        else:
            self.session.close()
            return {'Error':f'No match found for this id: {id}'}, 404
        
    def create_autorizzazione(self, nome:str, fkListaFunzionalita:str):
        try:
            autorizzazione = TAutorizzazioni(nome=nome, fkListaFunzionalita=fkListaFunzionalita)
            self.session.add(autorizzazione)
            self.session.commit()
            self.session.close()
            return {'Autorizzazione':'added!'}, 200
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}
        
    def update_autorizzazione(self, id:int, nome:str, fkListaFunzionalita:str):
        try:
            result = self.exists_autorizzazione(id)
            if result:
                result.nome = nome
                result.fkListaFunzionalita = fkListaFunzionalita
                self.session.commit()
                self.session.close()
                return {'Funzionalita':f'updated autorizzazione for this id: {id}, nome: {nome}, fkListaFunzionalita: {fkListaFunzionalita}'}, 200
            else:
                self.session.rollback()
                self.session.close()
                return {'Error':f'no match found for this id: {id}'}, 403
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500
        
    def delete_autorizzazione(self, id:int):
        try:
            result = self.exists_autorizzazione(id)
            if result:
                self.session.delete(result)
                self.session.commit()
                self.session.close()
                return {'Autorizzazione':f'deleted autorizzazione for this id: {id}'}
            else:
                self.session.rollback()
                self.session.close()
                return {'Error':f'no match found for this id: {id}'}, 403
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500