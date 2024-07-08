from Classi.ClasseUtility.UtilityUtenti.ConstantsUtenti import ConstantsUtenti

class UtilityUtenti:
    """Class for the utility of utenti"""

    # Empty Constructor
    def __init__(self) -> None:
        pass
    
    # Static methods
    @staticmethod
    def checkUsername(username:str):
        """
        :description: Static method to check if <utenti>username is None the function will raise a TypeError 
        and to check if <utenti>username is more than constants.MAX_LENGTH_USERNAME or it's an empty string
        the function will raise a ValueError or None if both of the above conditions are false
        :args: <utenti>username:str
        :return: None | raise ValueError | raise TypeError
        """
        if username is None:
            raise TypeError("username cannot be None!")
        constants = ConstantsUtenti()
        if (len(username.strip()) > constants.MAX_LENGTH_USERNAME) or (username.strip() == ""):
            raise ValueError(f"username cannot be empty or more than {constants.MAX_LENGTH_USERNAME} characters!")

    @staticmethod 
    def checkNome(nome:str):
        """
        :description: Static method to check if <utenti>nome is None the function will raise a TypeError 
        and to check if <utenti>nome is more than constants.MAX_LENGTH_NOME or it's an empty string
        the function will raise a ValueError or None if both of the above conditions are false
        :args: <utenti>nome:str
        :return: None | raise ValueError | raise TypeError
        """
        if nome is None:
            raise TypeError("nome cannot be None!")
        constants = ConstantsUtenti()
        if (len(nome.strip()) > constants.MAX_LENGTH_NOME) or (nome is None) or (nome.strip() == ""):
            raise ValueError(f"nome cannot be empty or more than {constants.MAX_LENGTH_NOME} characters!")

    @staticmethod
    def checkCognome(cognome:str):
        """
        :description: Static method to check if <utenti>cognome is None the function will raise a TypeError 
        and to check if <utenti>cognome is more than constants.MAX_LENGTH_COGNOME or it's an empty string
        the function will raise a ValueError or None if both of the above conditions are false
        :args: <utenti>cognome:str
        :return: None | raise ValueError | raise TypeError
        """
        if cognome is None:
            raise TypeError("cognome cannot be None!")
        constants = ConstantsUtenti()
        if (len(cognome.strip()) > constants.MAX_LENGTH_COGNOME) or (cognome.strip() == ""):
            raise ValueError(f"cognome cannot be empty or more than {constants.MAX_LENGTH_COGNOME} characters!")

    @staticmethod
    def checkFkTipoUtente(fkTipoUtente):
        """
        :description: Static method to check if <utenti>fkTipoUtente is None the function will raise a TypeError 
        and to check if <utenti>fkTipoUtente is less or equal to 0
        the function will raise a ValueError or None if both of the above conditions are false
        :args: <utenti>fkTipoUtente
        :return: None | raise ValueError | raise TypeError
        """
        if fkTipoUtente is None:
            raise TypeError("fkTipoUtente cannot be None!")
        if fkTipoUtente <= 0:
            raise ValueError("fkTipoUtente cannot be 0 or less than 0!")

    @staticmethod
    def checkFkFunzCustom(fkFunzCustom:str):
        """
        :description: Static method to check if <utenti>fkFunzCustom is None the function will return None 
        and to check if <utenti>fkFunzCustom is more than constants.MAX_LENGTH_FKFUNZCUSTOM the function will raise a ValueError
        :args: <utenti>fkFunzCustom:str
        :return: None | raise ValueError
        """
        if fkFunzCustom is None:
            return
        constants = ConstantsUtenti()
        if len(fkFunzCustom.strip()) > constants.MAX_LENGTH_FKFUNZCUSTOM:
            raise ValueError(f"fkFunzCustom cannot be more than {constants.MAX_LENGTH_FKFUNZCUSTOM} characters!")

    @staticmethod
    def checkReparti(reparti:str):
        """
        :description: Static method to check if <utenti>reparti is None the function will return None 
        and to check if <utenti>reparti is more than constants.MAX_LENGTH_REPARTI the function will raise a ValueError
        :args: <utenti>reparti:str
        :return: None | raise ValueError
        """
        if reparti is None:
            return
        constants = ConstantsUtenti()
        if len(reparti.strip()) > constants.MAX_LENGTH_REPARTI:
            raise ValueError(f"reparti cannot be more than {constants.MAX_LENGTH_REPARTI} characters!")

    @staticmethod
    def checkEmail(email:str):
        """
        :description: Static method to check if <utenti>cognome is None the function will raise a TypeError 
        and to check if <utenti>cognome is more than constants.MAX_LENGTH_EMAIL or it's an empty string or it doesn't contain a @
        the function will raise a ValueError or None if both of the above conditions are false
        :args: <utenti>cognome:str
        :return: None | raise ValueError | raise TypeError
        """
        if email is None:
            raise TypeError("email cannot be None!")
        if '@' not in email:
            raise ValueError('email must contain @!')
        constants = ConstantsUtenti()
        if (len(email.strip()) > constants.MAX_LENGTH_EMAIL) or (email is None) or (email.strip() == ""):
            raise ValueError(f"email cannot be empty or more than {constants.MAX_LENGTH_EMAIL} characters!")
        
    @staticmethod
    def checkPassword(password:str):
        """
        :description: Static method to check if <utenti>password is None the function will raise a TypeError 
        and to check if <utenti>password is more than constants.MAX_LENGTH_PASSWORD or it's an empty string
        the function will raise a ValueError or None if both of the above conditions are false
        :args: <utenti>password:str
        :return: None | raise ValueError | raise TypeError
        """
        if password is None:
            raise TypeError("password cannot be None!")
        constants = ConstantsUtenti()
        if (len(password.strip()) > constants.MAX_LENGTH_PASSWORD) or (password.strip() == ""):
            raise ValueError(f"password cannot be empty or more than {constants.MAX_LENGTH_PASSWORD} characters!")
        