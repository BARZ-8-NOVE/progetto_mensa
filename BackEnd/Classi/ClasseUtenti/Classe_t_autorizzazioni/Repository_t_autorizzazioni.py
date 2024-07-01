from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Domain_t_autorizzazioni import TAutorizzazioni
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages
from werkzeug.exceptions import NotFound

class Repository_t_autorizzazioni:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_autorizzazione(self, id):
        result = self.session.query(TAutorizzazioni).filter_by(id=id).first()
        return result

    def get_autorizzazioni_all(self):
        results = self.session.query(TAutorizzazioni).all()
        self.session.close()
        return UtilityGeneral.getClassDictionaryOrList(results)

    def get_autorizzazione_by_id(self, id:int):
            result = self.session.query(TAutorizzazioni).filter_by(id=id).first()
            if result:
                self.session.close()
                return UtilityGeneral.getClassDictionaryOrList(result)
            else:
                self.session.close()
                raise NotFound('Autorizzazione', 'id', id)
        
    def create_autorizzazione(self, nome:str, fkListaFunzionalita:str):
        result = TAutorizzazioni(nome=nome, fkListaFunzionalita=fkListaFunzionalita)
        self.session.add(result)
        self.session.commit()
        return UtilityGeneral.getClassDictionaryOrList(result)
        
    def update_autorizzazione(self, id:int, nome:str, fkListaFunzionalita:str):
        result:TAutorizzazioni = self.exists_autorizzazione(id)
        if result:
            result.nome = nome
            result.fkListaFunzionalita = fkListaFunzionalita
            self.session.commit()
            return UtilityGeneral.getClassDictionaryOrList(result)
        else:
            self.session.close()
            raise NotFound('Autorizzazione', 'id', id)
        
    def delete_autorizzazione(self, id:int):
            result = self.exists_autorizzazione(id)
            if result:
                self.session.delete(result)
                self.session.commit()
                self.session.close()
                return {'Autorizzazione': UtilityMessages.deleteMessage('Autorizzazione', 'id', id)}
            else:
                self.session.close()
                raise NotFound('Autorizzazione', 'id', id)