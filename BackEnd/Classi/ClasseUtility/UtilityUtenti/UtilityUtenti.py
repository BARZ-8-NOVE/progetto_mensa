from Classi.ClasseUtility.UtilityUtenti.ConstantsUtenti import ConstantsUtenti

class UtilityUtenti:

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def checkUsername(username:str):
        constants = ConstantsUtenti()
        if username is None:
            raise TypeError("username cannot be None!")
        if (len(username.strip()) > constants.MAX_LENGTH_USERNAME) or (username.strip() == ""):
            raise ValueError(f"username cannot be empty or more than {constants.MAX_LENGTH_USERNAME} characters!")

    @staticmethod 
    def checkNome(nome:str):
        constants = ConstantsUtenti()
        if nome is None:
            raise TypeError("nome cannot be None!")
        if (len(nome.strip()) > constants.MAX_LENGTH_NOME) or (nome is None) or (nome.strip() == ""):
            raise ValueError(f"nome cannot be empty or more than {constants.MAX_LENGTH_NOME} characters!")

    @staticmethod
    def checkCognome(cognome:str):
        constants = ConstantsUtenti()
        if cognome is None:
            raise TypeError("cognome cannot be None!")
        if (len(cognome.strip()) > constants.MAX_LENGTH_COGNOME) or (cognome.strip() == ""):
            raise ValueError(f"cognome cannot be empty or more than {constants.MAX_LENGTH_COGNOME} characters!")

    @staticmethod
    def checkFkTipoUtente(fkTipoUtente):
        if fkTipoUtente is None:
            raise TypeError("fkTipoUtente cannot be None!")
        if fkTipoUtente <= 0:
            raise ValueError("fkTipoUtente cannot be 0 or less than 0!")

    @staticmethod
    def checkFkFunzCustom(fkFunzCustom:str):
        constants = ConstantsUtenti()
        if len(fkFunzCustom.strip()) > constants.MAX_LENGTH_FKFUNZCUSTOM:
            raise ValueError(f"fkFunzCustom cannot be more than {constants.MAX_LENGTH_FKFUNZCUSTOM} characters!")

    @staticmethod
    def checkReparti(reparti:str):
        constants = ConstantsUtenti()
        if len(reparti.strip()) > constants.MAX_LENGTH_REPARTI:
            raise ValueError(f"reparti cannot be more than {constants.MAX_LENGTH_REPARTI} characters!")

    @staticmethod
    def checkEmail(email:str):
        constants = ConstantsUtenti()
        if email is None:
            raise TypeError("email cannot be None!")
        if (len(email.strip()) > constants.MAX_LENGTH_EMAIL) or (email is None) or (email.strip() == ""):
            raise ValueError(f"email cannot be empty or more than {constants.MAX_LENGTH_EMAIL} characters!")
        
    @staticmethod
    def checkPassword(password:str):
        constants = ConstantsUtenti()
        if password is None:
            raise TypeError("password cannot be None!")
        if (len(password.strip()) > constants.MAX_LENGTH_PASSWORD) or (password.strip() == ""):
            raise ValueError(f"password cannot be empty or more than {constants.MAX_LENGTH_PASSWORD} characters!")
        