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
    
    def exists_tipoUtente_by_nomeTipoUtente(self, nomeTipoUtente):
        result = self.session.query(TTipiUtenti).filter_by(nomeTipoUtente=nomeTipoUtente).first()
        return result.id
    
    def set_null_fkAutorizzazioni(self, fkAutorizzazioni):
        results = self.session.query(TTipiUtenti).filter_by(fkAutorizzazioni=fkAutorizzazioni).all()
        for result in results:
            result.fkAutorizzazioni = None
            self.session.commit()
        return
    
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
    
    def update_tipoUtente_nomeTipoUtente(self, id:int, nomeTipoUtente:str):
        tipoUtente:TTipiUtenti = self.exists_tipoUtente_by_id(id)
        if tipoUtente:
            tipoUtente.nomeTipoUtente = nomeTipoUtente
            self.session.commit()
        else:
            raise NotFound('TipoUtente', 'id', id)
        
    def update_tipoUtente_fkAutorizzazioni(self, id:int, fkAutorizzazioni):
        tipoUtente:TTipiUtenti = self.exists_tipoUtente_by_id(id)
        if tipoUtente:
            if fkAutorizzazioni:
                autorizzazione = Repository_t_autorizzazioni()
                result = autorizzazione.exists_autorizzazione(fkAutorizzazioni)
                if not result:
                    self.session.close()
                    raise NotFound('Autorizzazioni', 'fkAutorizzazioni', fkAutorizzazioni)
            tipoUtente.fkAutorizzazioni = fkAutorizzazioni
            self.session.commit()
            return
        else:
            raise NotFound('TipoUtente', 'id', id)
        
    def delete_tipoUtente(self, id:int):
        result = self.exists_tipoUtente_by_id(id)
        if result:
            from Classi.ClasseUtenti.Classe_t_utenti.Repository_t_utenti import Repository_t_utenti
            utenti = Repository_t_utenti()
            results = utenti.exist_utenti_by_tipoUtente(result.id)
            if not results:
                self.session.delete(result)
                self.session.commit()
                self.session.close()
                return
            else:
                return results
        else:
            self.session.close()
            raise NotFound('TipoUtente', 'id', id)
        