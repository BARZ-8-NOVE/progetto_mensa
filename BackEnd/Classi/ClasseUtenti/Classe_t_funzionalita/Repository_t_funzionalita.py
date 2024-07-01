from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages
from werkzeug.exceptions import NotFound

class Repository_t_funzionalita:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_funzionalita(self, id:int):
        result = self.session.query(TFunzionalita).filter_by(id=id).first()
        return result
        

    def get_funzionalita_all(self):
        results = self.session.query(TFunzionalita).all()
        self.session.close()
        return UtilityGeneral.getClassDictionaryOrList(results)

    def get_funzionalita_by_id(self, id:int):
        result = self.session.query(TFunzionalita).filter_by(id=id).first()
        if result:
            self.session.close()
            return UtilityGeneral.getClassDictionaryOrList(result)
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Funzionalita', 'id', id))
        
    def create_funzionalita(self, nome:str, frmNome:str):
        result = TFunzionalita(nome=nome, frmNome = frmNome)
        self.session.add(result)
        self.session.commit()
        return UtilityGeneral.getClassDictionaryOrList(result)
        
    def update_funzionalita(self, id:int, nome:str, frmNome:str):
            result:TFunzionalita = self.exists_funzionalita(id)
            if result:
                result.nome = nome
                result.frmNome = frmNome
                self.session.commit()
                return UtilityGeneral.getClassDictionaryOrList(result)
            else:
                self.session.close()
                raise NotFound(UtilityMessages.notFoundErrorMessage('Funzionalita', 'id', id))
        
    def delete_funzionalita(self, id:int):
        result = self.exists_funzionalita(id)
        if result:
            self.session.delete(result)
            self.session.commit()
            self.session.close()
            return {'Funzionalita':UtilityMessages.deleteMessage('Funzionalita', 'id', id)}
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Funzionalita', 'id', id))