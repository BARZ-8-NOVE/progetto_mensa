from Classi.ClasseDB.db_connection import Database

class t_utenti:

    # Costanti
    __MAX_USERNAME = 50
    __MAX_NOME = 50
    __MAX_COGNOME = 50

    # Costruttore vuoto
    def __init__(self) -> None:
        
        self.__Id = None
        self.__Username = None
        self.__Nome = None
        self.__Cognome = None
        self.__FkTipoUtente = None
        self.__FkFunzCustom = None
        self.__Reparti = None
        self.__Attivo = None
        self.__Inizio = None
        self.__Email = None
        self.__Password = None

    #Checks
    def checkUsername(self, username):
        if (len(username.strip()) > self.__MAX_USERNAME) or (username is None) or (username.strip() == ""):
            raise ValueError(f"L'username non può essere nullo o contenere più di {self.__MAX_USERNAME} caratteri!")
        
    def checkNome(self, nome):
        if (len(nome.strip()) > self.__MAX_NOME or (nome is None) or (nome.strip() == "")):
            raise ValueError(f"Il nome non può essere nullo o contenere più di {self.__MAX_NOME} caratteri!")
        
    def checkCognome(self, cognome):
        if (len(cognome.strip()) > self.__MAX_NOME or (cognome is None) or (cognome.strip() == "")):
            raise ValueError(f"Il cognome non può essere nullo o contenere più di {self.__MAX_COGNOME} caratteri!")

    def checkPositive(self, number):
        if number < 0:
            raise ValueError("Il numero deve essere maggiore di 0")

    def checkString(self, var):
        if not isinstance(var, str):
            raise TypeError("Deve essere una stringa!")
        
    def checkInt(self, var):
        if not isinstance(var, int):
            raise TypeError("Deve essere un intero!")

    # Getters
    @property
    def id(self):
        return self.__Id

    @property
    def username(self):
        return self.__Username

    @property
    def nome(self):
        return self.__Nome

    @property
    def cognome(self):
        return self.__Cognome

    @property
    def fkTipoUtente(self):
        return self.__FkTipoUtente

    @property
    def fkFunzCustom(self):
        return self.__FkFunzCustom

    @property
    def reparti(self):
        return self.__Reparti

    @property
    def attivo(self):
        return self.__Attivo

    @property
    def inizio(self):
        return self.__Inizio

    @property
    def email(self):
        return self.__Email

    @property
    def password(self):
        return self.__Password    

    # Setters
    @username.setter
    def username(self, username):
        self.__Username = username

    @nome.setter
    def nome(self, nome):
        self.checkString(nome)
        self.checkNome(nome)
        self.__Nome = nome

    @cognome.setter
    def cognome(self, cognome):
        self.checkString(cognome)
        self.checkCognome(cognome)
        self.__Cognome = cognome

    @fkTipoUtente.setter
    def fkTipoUtente(self, fkTipoUtente):
        self.__FkTipoUtente = fkTipoUtente

    @fkFunzCustom.setter
    def fkFunzCustom(self, fkFunzCustom):
        self.__FkFunzCustom = fkFunzCustom

    @reparti.setter
    def reparti(self, reparti):
        self.__Reparti = reparti

    @attivo.setter
    def attivo(self, attivo):
        self.__Attivo = attivo

    @inizio.setter
    def inizio(self, inizio):
        self.__Inizio = inizio

    @email.setter
    def email(self, email):
        self.__Email = email

    @password.setter
    def password(self, password):
        self.__Password = password
    
    