from Classi.ClasseUtenti.Classe_t_utenti.Repository_t_utenti import Repository_t_utenti
from Classi.ClasseUtility.UtilityUtenti.UtilityUtenti import UtilityUtenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente
from werkzeug.security import generate_password_hash
from datetime import datetime

class Service_t_utenti:

    def __init__(self) -> None:
        self.repository = Repository_t_utenti()
        
    def get_utenti_all(self):
        return self.repository.get_utenti_all()

    def get_all(self):
        return self.repository.get_all()

    def get_utente_by_id(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.get_utente_by_id(id)
    
    def get_utente_by_public_id(self, public_id : str):
        UtilityGeneral.checkId(id)
        return self.repository.get_utente_by_public_id(public_id)
    

    def get_reparti_list(self, user_id: int):
        return self.repository.get_reparti_list(user_id)
    
  
    def create_utente(self, username: str, nome: str, cognome: str, fkTipoUtente: str,
                    fkFunzCustom: str, reparti: str, email: str, password: str, inizio, fine):
        try:
            # Imposta stato predefinito e data di inizio
            attivo = 0
            inizio = datetime.now()  # Usa datetime.now() per ottenere la data corrente
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            # Creazione dell'utente nel repository
            return self.repository.create_utente(
                username=username,
                nome=nome,
                cognome=cognome,
                fkTipoUtente=fkTipoUtente,  # Assicurati che questo sia l'ID corretto se necessario
                fkFunzCustom=fkFunzCustom,
                reparti=reparti,
                attivo=attivo,
                email=email,
                password=hashed_password,
                inizio=inizio,
                fine=fine
            )

        except Exception as e:
            # Gestione degli errori
            raise Exception(f"An error occurred while creating the user: {str(e)}")

    
    def update_utente_username(self, id:int, username:str):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(username)
        return self.repository.update_utente_username(id, username)
    
    def update_utente_nome(self, id:int, nome:str):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(nome)
        return self.repository.update_utente_nome(id, nome)
    
    def update_utente_cognome(self, id:int, cognome:str):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(cognome)
        return self.repository.update_utente_cognome(id, cognome)
    
    def update_utente_fkTipoUtente(self, id:int, fkTipoUtente:int):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(fkTipoUtente)
        return self.repository.update_utente_fkTipoUtente(id, fkTipoUtente)
    
    def update_utente_fkFunzCustom(self, id:int, fkFunzCustom:str):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(fkFunzCustom)
        return self.repository.update_utente_fkFunzCustom(id, fkFunzCustom)
    
    def update_utente_reparti(self, id:int, reparti:str):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(reparti)
        return self.repository.update_utente_reparti(id, reparti)
    
    def update_utente_attivo(self, id:int, attivo:int):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(attivo)
        return self.repository.update_utente_attivo(id, attivo)
    
    def update_utente_password(self, id:int, password:str):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(password)
        return self.repository.update_utente_password(id, password)
    
    def update_utente_email(self, id:int, email:str):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(email)
        return self.repository.update_utente_email(id, email)

    def delete_utente(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.delete_utente(id)
    
    def do_login(self, username:str, password:str):
        UtilityUtenti.checkUsername(username)
        UtilityUtenti.checkPassword(password)
        return self.repository.do_login(username, password)
    
    def do_logout(self, current_utente_public_id:str):
        return self.repository.do_logout(current_utente_public_id)
    
    def do_logout_nuovo(self, id: int):
        return self.repository.do_logout_nuovo(id)
        
    
    def current_user(self, public_id):
        return self.repository.current_user(public_id)
    
    def expiredTokens(self):
        return self.repository.expiredTokens()
    
    def is_token_valid(self, id, token):
        return self.repository.is_token_valid(id, token)
    
    def update_da_pagina_admin(self, id, fkTipoUtente, reparti, inizio, fine):
        return self.repository.update_da_pagina_admin(id, fkTipoUtente, reparti, inizio, fine)
    
    def update_utente_password_by_username(self, username: str, password: str):
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        return self.repository.update_utente_password_by_username(username, hashed_password)
    
    def check_password(self, username: str, password: str):
        return self.repository.check_password(username, password)