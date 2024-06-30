from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

class Repository_t_funzionalita:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_funzionalita(self, id:int):
        try:
            result = self.session.query(TFunzionalita).filter_by(id=id).first()
            return UtilityGeneral.checkResult(result)
        except Exception as e:
            return {'Error':str(e)}, 400

    def get_funzionalita_all(self):
        try:
            results = self.session.query(TFunzionalita).all()
            self.session.close()
            return UtilityGeneral.getClassDictionary(results)
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500

    def get_funzionalita_by_id(self, id:int):
        try:
            result = self.session.query(TFunzionalita).filter_by(id=id).first()
            if result:
                self.session.close()
                return UtilityGeneral.getClassDictionary(result)
            else:
                self.session.close()
                return {'Error':f'cannot find funzionalita for this id: {id}'}, 404
        except Exception as e:
            return {'Error':str(e)}, 400
        
    def create_funzionalita(self, nome:str, frmNome:str):
        try:
            result = TFunzionalita(nome=nome, frmNome = frmNome)
            self.session.add(result)
            self.session.commit()
            return UtilityGeneral.getClassDictionary(result)
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}
        
    def update_funzionalita(self, id:int, nome:str, frmNome:str):
        try:
            result:TFunzionalita = self.exists_funzionalita(id)
            if result:
                result.nome = nome
                result.frmNome = frmNome
                self.session.commit()
                return UtilityGeneral.getClassDictionary(result)
            else:
                self.session.rollback()
                self.session.close()
                return {'Error':f'cannot find funzionalita for this id: {id}'}, 403
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
                return {'Error':f'cannot find funzionalita for this id: {id}'}, 403
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500

    
