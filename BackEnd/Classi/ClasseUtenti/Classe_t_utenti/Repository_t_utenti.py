from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages
from werkzeug.exceptions import Conflict, NotFound, Forbidden, Unauthorized
from werkzeug.security import check_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
import uuid
from datetime import datetime, timedelta

class Repository_t_utenti:
    
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_utente_by_username(self, username: str):
        result = self.session.query(TUtenti).filter_by(username=username).first()
        return result

    def exists_utente_by_id(self, id: int):
        result = self.session.query(TUtenti).filter_by(id=id).first()
        return result
    
    def exists_utente_by_email(self, email: str):
        result = self.session.query(TUtenti).filter_by(email=email).first()
        return result
    
    def exists_utente_by_email_with_different_id(self, email: str, id: int):
        result = self.session.query(TUtenti).filter(TUtenti.email == email, TUtenti.id != id).first()
        return result
    
    def exists_utente_by_username_with_different_id(self, username: str, id: int):
        result = self.session.query(TUtenti).filter(TUtenti.username == username, TUtenti.id != id).first()
        return result
    
    def exists_utente_by_public_id(self, public_id):
        result = self.session.query(TUtenti).filter_by(public_id=public_id).first()
        return result
    
    def exist_utenti_by_tipoUtente(self, fkTipoUtente):
        results = self.session.query(TUtenti).filter_by(fkTipoUtente=fkTipoUtente).all()
        return results
    
    def get_utenti_all(self):
        results = self.session.query(TUtenti).all()
        self.session.close()
        return UtilityGeneral.getClassDictionaryOrList(results)

    def get_utente_by_id(self, id: int):
        result = self.session.query(TUtenti).filter_by(id=id).first()
        if result:
            self.session.close()
            return UtilityGeneral.getClassDictionaryOrList(result)
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def create_utente(self, username: str, nome: str, cognome: str, fkTipoUtente: int,
                      fkFunzCustom: str, reparti: str, attivo: int, inizio, email: str, password: str):
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
        utente = TUtenti(public_id=str(uuid.uuid4()), username=username, nome=nome, cognome=cognome, fkTipoUtente=fkTipoUtente,
                         fkFunzCustom=fkFunzCustom, reparti=reparti, attivo=attivo, inizio=inizio,
                         email=email, password=password)
        self.session.add(utente)
        self.session.commit()
        return UtilityGeneral.getClassDictionaryOrList(utente)
    
    def update_utente_username(self, id: int, username: str):
        utente: TUtenti = self.exists_utente_by_id(id)
        if utente:
            result_exists_utente_by_username_with_different_id = self.exists_utente_by_username_with_different_id(username, id)
            if result_exists_utente_by_username_with_different_id:
                self.session.close()    
                raise Conflict(UtilityMessages.existsErrorMessage('Utente', 'username', username))
            utente.username = username
            self.session.commit()
            return
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def update_utente_email(self, id: int, email: str):
        utente: TUtenti = self.exists_utente_by_id(id)
        if utente:
            result_exists_utente_by_email_with_different_id = self.exists_utente_by_email_with_different_id(email, id)
            if result_exists_utente_by_email_with_different_id:
                self.session.close()
                raise Conflict(UtilityMessages.existsErrorMessage('Utente', 'email', email))
            utente.email = email
            self.session.commit()
            return
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def update_utente_fkTipoUtente(self, id: int, fkTipoUtente: int):
        utente: TUtenti = self.exists_utente_by_id(id)
        if utente:
            tipoUtente = Repository_t_tipiUtente()
            result = tipoUtente.exists_tipoUtente_by_id(fkTipoUtente)
            if not result:
                self.session.close()
                raise NotFound(UtilityMessages.notFoundErrorMessage('TipoUtente', 'fkTipoUtente', fkTipoUtente))
            utente.fkTipoUtente = fkTipoUtente
            self.session.commit()
            return
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def update_utente_nome(self, id: int, nome: str):
        utente: TUtenti = self.exists_utente_by_id(id)
        if utente:
            utente.nome = nome
            self.session.commit()
            return
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def update_utente_cognome(self, id: int, cognome: str):
        utente: TUtenti = self.exists_utente_by_id(id)
        if utente:
            utente.cognome = cognome
            self.session.commit()
            return
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def update_utente_fkFunzCustom(self, id: int, fkFunzCustom: str):
        utente: TUtenti = self.exists_utente_by_id(id)
        if utente:
            utente.fkFunzCustom = fkFunzCustom
            self.session.commit()
            return
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def update_utente_reparti(self, id: int, reparti: str):
        utente: TUtenti = self.exists_utente_by_id(id)
        if utente:
            utente.reparti = reparti
            self.session.commit()
            return
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def update_utente_password(self, id: int, password: str):
        utente: TUtenti = self.exists_utente_by_id(id)
        if utente:
            utente.password = password
            self.session.commit()
            return
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))

    def update_utente_attivo(self, id: int, attivo):
        utente: TUtenti = self.exists_utente_by_id(id)
        if utente:
            utente.attivo = attivo
            self.session.commit()
            return
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def delete_utente(self, id: int):
        result = self.exists_utente_by_id(id)
        if result:
            self.session.delete(result)
            self.session.commit()
            self.session.close()
            return {'utente': UtilityMessages.deleteMessage('Utente', 'id', id)}
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        
    def do_login(self, username: str, password: str, token_expires=timedelta(minutes=30)):
        result = self.exists_utente_by_username(username)
        if result:
            hashed_password = result.password
            if hashed_password and check_password_hash(hashed_password, password):
                if result.attivo == 0:
                    self.update_utente_attivo(result.id, 1)
                    access_token = create_access_token(identity=result.public_id, expires_delta=token_expires)
                    response = jsonify(access_token=access_token)
                    set_access_cookies(response=response, encoded_access_token=access_token)
                    result.token = access_token
                    result.expires = datetime.now() + token_expires
                    self.session.commit()
                    return {'id': result.id, 'token': access_token, 'username': username, 'reparti': result.reparti,
                            'nome': result.nome, 'cognome': result.cognome, 'email': result.email,
                            'fkTipoUtente': result.fkTipoUtente}
                else:
                    self.update_utente_attivo(result.id, 0)
                    self.session.close()
                    raise Forbidden(UtilityMessages.forbiddenUtenteAlreadyLoggedInError(username, 'in'))
            else:
                self.session.close()
                raise Forbidden(UtilityMessages.forbiddenPasswordIncorrectError(username))
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'username', username))
        
    def do_logout(self, current_utente_public_id: str):
        result = self.exists_utente_by_public_id(current_utente_public_id)
        if result:
            if result.attivo == 1:
                self.update_utente_attivo(result.id, 0)
                return UtilityGeneral.getClassDictionaryOrList(result)
            else:
                self.session.close()
                raise Forbidden(UtilityMessages.forbiddenUtenteAlreadyLoggedInError(result.username, 'out'))
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'username', result.username))
        
    def current_user(self, public_id):
        current_user = self.session.query(TUtenti).filter_by(public_id=public_id).first()
        if not current_user:
            raise Unauthorized(UtilityMessages.unauthorizedErrorToken('invalid'))
        return current_user
    
    def expiredTokens(self):
        expired_tokens = self.session.query(TUtenti).filter(TUtenti.expires < datetime.now()).all()
        for utente in expired_tokens:
            utente.attivo = 0
            print(f"Removing expired token for user {utente.username}")
            utente.expires = None
            utente.token = None
        self.session.commit()

    def get_utente_by_username_and_password(self, username: str, password: str):
        # Check if user exists by username
        utente = self.exists_utente_by_username(username)
        if utente:
            # Verify password
            if check_password_hash(utente.password, password):
                return UtilityGeneral.getClassDictionaryOrList(utente)  # Return user details
            else:
                raise Forbidden(UtilityMessages.forbiddenPasswordIncorrectError(username))
        else:
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'username', username))


    def get_utente_by_public_id (self, public_id: str):
        result = self.session.query(TUtenti).filter_by(public_id = public_id).first()
        if result:
            self.session.close()
            return UtilityGeneral.getClassDictionaryOrList(result)
        else:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'id', id))
        