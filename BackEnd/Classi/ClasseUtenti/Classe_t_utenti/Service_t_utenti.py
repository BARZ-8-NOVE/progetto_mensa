from Classi.ClasseUtenti.Classe_t_utenti.Repository_t_utenti import Repository_t_utenti
from datetime import datetime

class Service_t_utenti:

    __MAX_LENGTH_USERNAME = 50
    __MAX_LENGTH_NOME = 50
    __MAX_LENGTH_COGNOME = 50
    __MAX_LENGTH_FKFUNZCUSTOM = 1000
    __MAX_LENGTH_REPARTI = 1000
    __MAX_LENGTH_EMAIL = 255
    __MAX_LENGTH_PASSWORD = 255

    def __init__(self) -> None:
        self.repository = Repository_t_utenti()
        date = datetime.now()
        self.Date = date.strftime("%Y-%m-%d")

    def __checkUsername(self, username:str):
        if (len(username.strip()) > self.__MAX_LENGTH_USERNAME) or (username is None) or (username.strip() == ""):
            raise ValueError(f"username cannot be None or more than {self.__MAX_LENGTH_USERNAME} characters!")
        
    def __checkNome(self, nome:str):
        if (len(nome.strip()) > self.__MAX_LENGTH_NOME) or (nome is None) or (nome.strip() == ""):
            raise ValueError(f"nome cannot be None or more than {self.__MAX_LENGTH_NOME} characters!")
        
    def __checkCognome(self, cognome:str):
        if (len(cognome.strip()) > self.__MAX_LENGTH_COGNOME) or (cognome is None) or (cognome.strip() == ""):
            raise ValueError(f"cognome cannot be None or more than {self.__MAX_LENGTH_COGNOME} characters!")

    def __checkFkTipoUtente(self, fkTipoUtente:int):
        if fkTipoUtente is None or fkTipoUtente < 0:
            raise ValueError("fkTipoUtente cannot be None or less than 0!")

    def __checkFkFunzCustom(self, fkFunzCustom:str):
        if len(fkFunzCustom.strip()) > self.__MAX_LENGTH_FKFUNZCUSTOM:
            raise ValueError(f"fkFunzCustom cannot be more than {self.__MAX_LENGTH_FKFUNZCUSTOM} characters!")

    def __checkReparti(self, reparti:str):
        if len(reparti.strip()) > self.__MAX_LENGTH_REPARTI:
            raise ValueError(f"reparti cannot be more than {self.__MAX_LENGTH_REPARTI} characters!")

    def __checkEmail(self, email:str):
        if (len(email.strip()) > self.__MAX_LENGTH_EMAIL) or (email is None) or (email.strip() == ""):
            raise ValueError(f"email cannot be None or more than {self.__MAX_LENGTH_EMAIL} characters!")
        
    def __checkPassword(self, password:str):
        if (len(password.strip()) > self.__MAX_LENGTH_PASSWORD) or (password is None) or (password.strip() == ""):
            raise ValueError(f"password cannot be more than {self.__MAX_LENGTH_PASSWORD} characters!")

    def __checkId(self, id:int):
        if (id is None) or (id < 0) or (id == 0):
            raise ValueError("id cannot be None, 0, or less than 0!")
        
    def get_utenti_all(self):
        return self.repository.get_utenti_all()

    def get_utente_by_id(self, id:int):
        self.__checkId(id)
        return self.repository.get_utente_by_id(id)
    
    def create_utente(self, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, email:str, password:str):
        self.__checkUsername(username)
        self.__checkNome(nome)
        self.__checkCognome(cognome)
        self.__checkFkTipoUtente(fkTipoUtente)
        self.__checkFkFunzCustom(fkFunzCustom)
        self.__checkReparti(reparti)
        attivo = 0
        inizio = self.Date
        self.__checkEmail(email)
        self.__checkPassword(password)
        return self.repository.create_utente(username, nome, cognome, fkTipoUtente,
                    fkFunzCustom, reparti, attivo, inizio, email, password)
    
    def update_utente(self, id:int, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, attivo:int, email:str, password:str):
        self.__checkId(id)
        self.__checkUsername(username)
        self.__checkNome(nome)
        self.__checkCognome(cognome)
        self.__checkFkTipoUtente(fkTipoUtente)
        self.__checkFkFunzCustom(fkFunzCustom)
        self.__checkReparti(reparti)
        inizio = self.Date
        self.__checkEmail(email)
        self.__checkPassword(password)
        return self.repository.update_utente(id, username, nome, cognome, fkTipoUtente,
                    fkFunzCustom, reparti, attivo, inizio, email, password)
    
    def delete_utente(self, id:int):
        self.__checkId(id)
        return self.repository.delete_utente(id)