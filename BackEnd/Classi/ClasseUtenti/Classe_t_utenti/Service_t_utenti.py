from Classi.ClasseUtenti.Classe_t_utenti.Repository_t_utenti import Repository_t_utenti
from Classi.ClasseUtility.UtilityUtenti.UtilityUtenti import UtilityUtenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

class Service_t_utenti:

    def __init__(self) -> None:
        self.repository = Repository_t_utenti()
        
    def get_utenti_all(self):
        return self.repository.get_utenti_all()

    def get_utente_by_id(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.get_utente_by_id(id)
    
    def create_utente(self, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, email:str, password:str):
        UtilityUtenti.checkUsername(username)
        UtilityUtenti.checkNome(nome)
        UtilityUtenti.checkCognome(cognome)
        UtilityUtenti.checkFkTipoUtente(fkTipoUtente)
        UtilityUtenti.checkFkFunzCustom(fkFunzCustom)
        UtilityUtenti.checkReparti(reparti)
        attivo = 0
        inizio = UtilityGeneral.current_date()
        UtilityUtenti.checkEmail(email)
        UtilityUtenti.checkPassword(password)
        return self.repository.create_utente(username, nome, cognome, fkTipoUtente,
                    fkFunzCustom, reparti, attivo, inizio, email, password)
    
    def update_utente_searched_by_id(self, id:int, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, attivo:int, email:str, password:str):
        UtilityGeneral.checkId(id)
        UtilityUtenti.checkUsername(username)
        UtilityUtenti.checkNome(nome)
        UtilityUtenti.checkCognome(cognome)
        UtilityUtenti.checkFkTipoUtente(fkTipoUtente)
        UtilityUtenti.checkFkFunzCustom(fkFunzCustom)
        UtilityUtenti.checkReparti(reparti)
        UtilityUtenti.checkEmail(email)
        UtilityUtenti.checkPassword(password)
        return self.repository.update_utente_searched_by_id(id, username, nome, cognome, fkTipoUtente,
                    fkFunzCustom, reparti, attivo, email, password)
    
    def delete_utente(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.delete_utente(id)