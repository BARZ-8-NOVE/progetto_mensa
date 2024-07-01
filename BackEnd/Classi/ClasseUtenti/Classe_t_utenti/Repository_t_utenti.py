from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages
from werkzeug.exceptions import Conflict, NotFound

class Repository_t_utenti:
    
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_utente_by_id(self, id:int):
        result = self.session.query(TUtenti).filter_by(id=id).first()
        return result
        
    def exists_utente_by_username(self, username:str):
        result = self.session.query(TUtenti).filter_by(username=username).first()
        return result
        
    def exists_utente_by_email(self, email:str):
        result = self.session.query(TUtenti).filter_by(email=email).first()
        return result
    
    def exists_utente_by_email_with_different_id(self, email:str, id:int):
        result = self.session.query(TUtenti).filter(TUtenti.email==email, TUtenti.id!=id).first()
        return result
    
    def exists_utente_by_username_with_different_id(self, username:str, id:int):
        result = self.session.query(TUtenti).filter(TUtenti.username==username, TUtenti.id!=id).first()
        return result
    
    def get_utenti_all(self):
        results = self.session.query(TUtenti).all()
        self.session.close()
        return UtilityGeneral.getClassDictionaryOrList(results)

    def get_utente_by_id(self, id:int):
        result = self.session.query(TUtenti).filter_by(id=id).first()
        if result:
            self.session.close()
            return UtilityGeneral.getClassDictionaryOrList(result)
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def create_utente(self, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, attivo:int, inizio, email:str, password:str):
        resultExistsEmail = self.exists_utente_by_email(email)
        if resultExistsEmail:
            self.session.close()
            raise Conflict(UtilityMessages.existsErrorMessage('Utente', 'email', email))
        resultExistsUsername = self.exists_utente_by_username(username)
        if resultExistsUsername:
            self.session.close()
            raise Conflict(UtilityMessages.existsErrorMessage('Utente', 'username', username))
        tipoUtente = Repository_t_tipiUtente()
        resultTipoUtente = tipoUtente.exists_tipoUtente_by_id(fkTipoUtente)
        if not resultTipoUtente:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('TipoUtente', 'fkTipoUtente', fkTipoUtente))
        utente = TUtenti(username=username, nome=nome, cognome=cognome, fkTipoUtente=fkTipoUtente,
                        fkFunzCustom=fkFunzCustom, reparti=reparti, attivo=attivo, inizio=inizio,
                        email=email, password=password)
        self.session.add(utente)
        self.session.commit()
        return UtilityGeneral.getClassDictionaryOrList(utente)
        
    def update_utente(self, id:int, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, attivo, email:str, password:str):
        utente:TUtenti = self.exists_utente_by_id(id)
        if utente:
            result_exists_utente_by_email_with_different_id = self.exists_utente_by_email_with_different_id(email, id)
            if result_exists_utente_by_email_with_different_id:
                self.session.close()
                raise Conflict(UtilityMessages.existsErrorMessage('Utente', 'email', email))
            result_exists_utente_by_username_with_different_id = self.exists_utente_by_username_with_different_id(username, id)
            if result_exists_utente_by_username_with_different_id:
                self.session.close()    
                raise Conflict(UtilityMessages.existsErrorMessage('Utente', 'username', username))            
            tipoUtente = Repository_t_tipiUtente()
            result = tipoUtente.exists_tipoUtente_by_id(fkTipoUtente)
            if not result:
                self.session.close()
                raise NotFound(UtilityMessages.notFoundErrorMessage('TipoUtente', 'fkTipoUtente', fkTipoUtente))
            utente.username = username
            utente.nome = nome
            utente.cognome = cognome
            utente.fkTipoUtente = fkTipoUtente
            utente.fkFunzCustom = fkFunzCustom
            utente.reparti = reparti
            utente.attivo = attivo
            utente.email = email
            utente.password = password
            self.session.commit()
            return UtilityGeneral.getClassDictionaryOrList(utente)
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def delete_utente(self, id:int):
        result = self.exists_utente_by_id(id)
        if result:
            self.session.delete(result)
            self.session.commit()
            self.session.close()
            return {'utente': UtilityMessages.deleteMessage('Utente', 'id', id)}
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))