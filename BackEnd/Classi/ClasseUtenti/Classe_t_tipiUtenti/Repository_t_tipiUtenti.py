from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Domain_t_tipiUtenti import TTipiUtenti
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Repository_t_autorizzazioni import Repository_t_autorizzazioni
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages
from werkzeug.exceptions import NotFound

class Repository_t_tipiUtente:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_tipoUtente_by_id(self, id:int):
        result = self.session.query(TTipiUtenti).filter_by(id=id).first()
        return result
    
    def get_tipiUtenti_all(self):
        results = self.session.query(TTipiUtenti).all()
        self.session.close()
        return UtilityGeneral.getClassDictionaryOrList(results)

    def get_tipoUtente_by_id(self, id:int):
        result = self.session.query(TTipiUtenti).filter_by(id=id).first()
        if result:
            self.session.close()
            return UtilityGeneral.getClassDictionaryOrList(result)
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('TipoUtente', 'id', id))
        
    def create_tipoUtente(self, nomeTipoUtente:str, fkAutorizzazioni):
        if fkAutorizzazioni:
            autorizzazione = Repository_t_autorizzazioni()
            result = autorizzazione.exists_autorizzazione(fkAutorizzazioni)
            if not result:
                self.session.close()
                raise NotFound(UtilityMessages.notFoundErrorMessage('Autorizzazioni', 'fkAutorizzazioni', fkAutorizzazioni))
        tipoUtente = TTipiUtenti(nomeTipoUtente=nomeTipoUtente, fkAutorizzazioni=fkAutorizzazioni)
        self.session.add(tipoUtente)
        self.session.commit()
        return UtilityGeneral.getClassDictionaryOrList(tipoUtente)
        
    def update_tipoUtente(self, id:int, nomeTipoUtente:str, fkAutorizzazioni):
        tipoUtente:TTipiUtenti = self.exists_tipoUtente_by_id(id)
        if tipoUtente:
            if fkAutorizzazioni:
                autorizzazione = Repository_t_autorizzazioni()
                result = autorizzazione.exists_autorizzazione(fkAutorizzazioni)
                if not result:
                    self.session.close()
                    raise NotFound('Autorizzazioni', 'fkAutorizzazioni', fkAutorizzazioni)
            tipoUtente.nomeTipoUtente = nomeTipoUtente
            tipoUtente.fkAutorizzazioni = fkAutorizzazioni
            self.session.commit()
            return UtilityGeneral.getClassDictionaryOrList(tipoUtente), 200
        else:
            raise NotFound('TipoUtente', 'id', id)
        
    def delete_tipoUtente(self, id:int):
        result = self.exists_tipoUtente_by_id(id)
        if result:
            self.session.delete(result)
            self.session.commit()
            self.session.close()
            return {'TipoUtente': UtilityMessages.deleteMessage('TipiUtente', 'id', id)}
        else:
            self.session.rollback()
            self.session.close()
            raise NotFound('TipoUtente', 'id', id)
        