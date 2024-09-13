from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages
from werkzeug.exceptions import Conflict, NotFound, Forbidden, Unauthorized
from werkzeug.security import check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
import uuid
from datetime import date, datetime, timedelta, timezone
import logging
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
    



    def get_all(self):
        try:
            results = self.session.query(TUtenti).all()
            return [{
                'id': result.id,
                'public_id': result.public_id,
                'username': result.username,
                'nome': result.nome,
                'cognome': result.cognome,
                'fkTipoUtente': result.fkTipoUtente,
                'fkFunzCustom': result.fkFunzCustom,
                'reparti': result.reparti,
                'attivo': result.attivo,  # Mantiene l'ora e i minuti
                'inizio': result.inizio.date() if isinstance(result.inizio, datetime) else result.inizio,
                'fine': result.fine.date() if isinstance(result.fine, datetime) else result.fine,
                'email': result.email
            } for result in results]
        except Exception as e:
            logging.error(f"Error getting all alimenti: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()





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


    def get_reparti_list(self, user_id: int):
        try:
            # Recupera l'utente dalla sessione
            user = self.session.query(TUtenti).filter_by(id=user_id).first()
            
            if user:
                # Verifica se l'attributo reparti è None o una stringa vuota
                if user.reparti:
                    # Converte la stringa dei reparti in una lista di interi
                    reparti_list = [int(reparto_id) for reparto_id in user.reparti.split(',')]
                else:
                    # Restituisce una lista vuota se reparti è None o vuoto
                    reparti_list = []
                
                # Chiudi la sessione
                self.session.close()
                return reparti_list
            else:
                # Chiudi la sessione e solleva un'eccezione se l'utente non viene trovato
                self.session.close()
                raise NotFound(f"Utente con ID {user_id} non trovato.")
        except Exception as e:
            # Gestisci eccezioni generali e chiudi la sessione
            self.session.close()
            raise RuntimeError(f"An error occurred while retrieving the user's reparti: {str(e)}")






    def create_utente(self, username: str, nome: str, cognome: str, fkTipoUtente: int,
                  fkFunzCustom: str, reparti: str, attivo: int, inizio, email: str, password: str, fine):
        try:
            # Log dei dati di input
            print(f"Creating user with: username={username}, nome={nome}, cognome={cognome}, fkTipoUtente={fkTipoUtente}, fkFunzCustom={fkFunzCustom}, reparti={reparti}, attivo={attivo}, inizio={inizio}, email={email}")

            # Verifica se l'email esiste già
            if self.exists_utente_by_email(email):
                raise Conflict(UtilityMessages.existsErrorMessage('Utente', 'email', email))
            
            # Verifica se l'username esiste già
            if self.exists_utente_by_username(username):
                raise Conflict(UtilityMessages.existsErrorMessage('Utente', 'username', username))
            
            # Verifica se il tipo di utente esiste
            tipoUtente = Repository_t_tipiUtente()
            if not tipoUtente.exists_tipoUtente_by_id(fkTipoUtente):
                raise NotFound(UtilityMessages.notFoundErrorMessage('TipoUtente', 'fkTipoUtente', fkTipoUtente))
            
            # Creazione dell'oggetto utente
            utente = TUtenti(
                public_id=str(uuid.uuid4()),
                username=username,
                nome=nome,
                cognome=cognome,
                fkTipoUtente=fkTipoUtente,
                fkFunzCustom=','.join(map(str, fkFunzCustom)) if isinstance(fkFunzCustom, list) else fkFunzCustom,
                reparti=','.join(map(str, reparti)) if isinstance(reparti, list) else reparti,
                attivo=attivo,
                inizio=inizio,
                email=email,
                fine=fine,
                password=password
            )

            # Log dell'oggetto utente
            print(f"User object to be added: {utente}")

            # Aggiunta e commit dell'utente al database
            self.session.add(utente)
            self.session.commit()
            
            return UtilityGeneral.getClassDictionaryOrList(utente)
        
        except SQLAlchemyError as e:
            # Rollback in caso di errore durante la transazione
            self.session.rollback()
            print(f"Exception occurred: {str(e)}")  # Log dell'errore
            raise RuntimeError(f"An error occurred while creating the user: {str(e)}")
        
        finally:
            # Assicurati che la sessione venga chiusa
            if self.session:
                self.session.close()







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
        

    def update_utente_password_by_username(self, username: str, password: str):
        utente: TUtenti = self.exists_utente_by_username(username)
        if utente:
            utente.password = password
            self.session.commit()
            return
        else:
             raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'username', username))

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
        
        if not result:
            self.session.close()
            raise NotFound(UtilityMessages.notFoundErrorMessage('Utente', 'username', username))

        hashed_password = result.password
        if not (hashed_password and check_password_hash(hashed_password, password)):
            self.session.close()
            raise Forbidden(UtilityMessages.forbiddenPasswordIncorrectError(username))

        # Controlla se l'utente è scaduto
        if result.fine is not None and isinstance(result.fine, datetime) and result.fine.date() < date.today():
            self.session.close()
            raise Forbidden(UtilityMessages.utenteScadutoError(username))
        
        # Se l'utente non è attivo, aggiorna lo stato e genera un nuovo token
        if result.attivo == 0:
            self.update_utente_attivo(result.id, 1)
            access_token = create_access_token(identity=result.public_id, expires_delta=token_expires)
            response = jsonify(access_token=access_token)
            set_access_cookies(response=response, encoded_access_token=access_token)
            result.token = access_token
            result.expires = datetime.now() + token_expires
            self.session.commit()
        else:
            access_token = result.token  # Usa il token esistente se l'utente è già attivo

        # Prepara l'oggetto utente
        utente = {
            'id': result.id,
            'token': access_token,
            'username': username,
            'reparti': result.reparti,
            'nome': result.nome,
            'cognome': result.cognome,
            'email': result.email,
            'fkTipoUtente': result.fkTipoUtente,
            'fine': result.fine
        }
        return utente
    



    def check_password(self, username: str, password: str):
        # Recupera l'utente dal database usando il nome utente
        user = self.exists_utente_by_username(username)
        
        # Se l'utente non esiste, chiudi la sessione e solleva un'eccezione NotFound
        if not user:
            self.session.close()
            raise NotFound(f"Utente con username '{username}' non trovato.")
        
        # Verifica la password confrontando l'hash della password memorizzata
        hashed_password = user.password
        if not (hashed_password and check_password_hash(hashed_password, password)):
            self.session.close()
            raise Forbidden("La password fornita è errata.")
        
        # Chiudi la sessione dopo la verifica
        self.session.close()
        return True

        
        
        


        


    def do_logout_nuovo(self, id: int):
        # Trova l'utente nel database utilizzando l'user_id
        utente = self.session.query(TUtenti).filter(TUtenti.id == id).first()
        
        if utente:
            # Imposta il token come scaduto
            utente.expires = None  # Imposta la scadenza del token alla data e ora attuale
            utente.token = None  # Puoi anche rimuovere il token, se necessario
            
            # Imposta l'utente come inattivo (opzionale, dipende dal contesto)
            utente.attivo = 0
            
            # Salva le modifiche nel database
            self.session.commit()
            
            print(f"User {utente.username} has logged out and token has been invalidated.")
        else:
            print(f"User with ID {id} not found.")



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
        

    def is_token_valid(self, id, token):
        # Recupera l'utente dal database usando il suo public_id
        user = self.session.query(TUtenti).filter_by(id = id).first()
        if not user:
            return False

        # Confronta il token attuale con quello salvato nel database
        return user.token == token


    def update_da_pagina_admin(self, id, fkTipoUtente: int, reparti: list, inizio, fine):
        try:
            print(f"Updating user with id: {id}")
            Utente = self.session.query(TUtenti).filter_by(id=id).first()
            if Utente:
                print(f"Found user: {Utente}")
                Utente.fkTipoUtente = fkTipoUtente
                Utente.reparti = ','.join(map(str, reparti)) if isinstance(reparti, list) else reparti

                # Gestisci i valori vuoti per le colonne DATE/DATETIME
                Utente.inizio = inizio if inizio else None
                Utente.fine = fine if fine else None

                print("Committing transaction")
                self.session.commit()
                return {'Message': 'utente updated successfully!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()






    def manage_token(self, id, token, token_expires=timedelta(minutes=30)):
        # Recupera l'utente dal database usando l'ID
        user = self.session.query(TUtenti).filter_by(id=id).first()
        if not user:
            raise ValueError("Utente non trovato")

        # Verifica se il token salvato nel database corrisponde a quello passato
        if user.token != token:
            raise ValueError("Token non valido")

        # Verifica se la data di scadenza del token è valida
        if user.expires and isinstance(user.expires, datetime):
            current_time = datetime.now()  # Usa datetime "naive"
            # Calcola il tempo rimanente fino alla scadenza
            time_remaining = user.expires - current_time
            # Soglia di 5 minuti
            threshold = timedelta(minutes=5)

            if current_time > user.expires:
                raise ValueError("Il token è scaduto")

            if time_remaining <= threshold:
                # Rinnova il token se sta per scadere
                expires = current_time + token_expires
                new_token = create_access_token(identity=user.public_id, expires_delta=token_expires)

                # Aggiorna il token e la scadenza nel database
                user.token = new_token
                user.expires = expires
                self.session.commit()

                # Prepara la risposta
                response = jsonify(token=new_token)
                set_access_cookies(response, encoded_access_token=new_token)
                return response

        # Se il token non è vicino alla scadenza, restituisce un messaggio di successo senza rinnovo
        return jsonify(message="Token is valid and not near expiration")
