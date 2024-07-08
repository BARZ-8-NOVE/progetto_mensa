from Classi.ClasseUtenti.Classe_t_utenti.Repository_t_utenti import Repository_t_utenti
from Classi.ClasseUtility.UtilityUtenti.UtilityUtenti import UtilityUtenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente
from werkzeug.security import generate_password_hash

class Service_t_utenti:

    def __init__(self) -> None:
        self.repository = Repository_t_utenti()
        
    def get_utenti_all(self):
        return self.repository.get_utenti_all()

    def get_utente_by_id(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.get_utente_by_id(id)
    
    def create_utente(self, username:str, nome:str, cognome:str, nomeTipoUtente,
                    fkFunzCustom:str, reparti:str, email:str, password:str):
        UtilityUtenti.checkUsername(username)
        UtilityUtenti.checkNome(nome)
        UtilityUtenti.checkCognome(cognome)
        tipoUtente = Repository_t_tipiUtente()
        fkTipoUtente = tipoUtente.exists_tipoUtente_by_nomeTipoUtente(nomeTipoUtente)
        UtilityUtenti.checkFkTipoUtente(fkTipoUtente)
        UtilityUtenti.checkFkFunzCustom(fkFunzCustom)
        UtilityUtenti.checkReparti(reparti)
        attivo = 0
        inizio = UtilityGeneral.current_date()
        UtilityUtenti.checkEmail(email)
        UtilityUtenti.checkPassword(password)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        return self.repository.create_utente(username, nome, cognome, fkTipoUtente, fkFunzCustom, reparti, attivo, inizio, email, hashed_password)
    
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
    
    def current_user(self, public_id):
        return self.repository.current_user(public_id)
    
    def expiredTokens(self):
        return self.repository.expiredTokens()