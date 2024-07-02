class ConstantsUtenti:
    """Class for the constants of utenti"""

    # Empty Constructor
    def __init__(self) -> None:
        pass
    
    # Constants
    __MAX_LENGTH_USERNAME = 50
    __MAX_LENGTH_NOME = 50
    __MAX_LENGTH_COGNOME = 50
    __MAX_LENGTH_FKFUNZCUSTOM = 1000
    __MAX_LENGTH_REPARTI = 1000
    __MAX_LENGTH_EMAIL = 255
    __MAX_LENGTH_PASSWORD = 255
    
    #Getters
    @property
    def MAX_LENGTH_USERNAME(self):
        """
        :description: Getter of the constant for the max length of the <utenti>username
        :return: self.__MAX_LENGTH_USERNAME, LITERAL[50]
        """
        return self.__MAX_LENGTH_USERNAME
    
    @property
    def MAX_LENGTH_NOME(self):
        """
        :description: Getter of the constant for the max length of the <utenti>nome
        :return: self.__MAX_LENGTH_NOME, LITERAL[50]
        """
        return self.__MAX_LENGTH_NOME
    
    @property
    def MAX_LENGTH_COGNOME(self):
        """
        :description: Getter of the constant for the max length of the <utenti>cognome
        :return: self.__MAX_LENGTH_COGNOME, LITERAL[50]
        """
        return self.__MAX_LENGTH_COGNOME
    
    @property
    def MAX_LENGTH_FKFUNZCUSTOM(self):
        """
        :description: Getter of the constant for the max length of the <utenti>fkFunzCustom
        :return: self.__MAX_LENGTH_FKFUNZCUSTOM, LITERAL[1000]
        """
        return self.__MAX_LENGTH_FKFUNZCUSTOM
    
    @property
    def MAX_LENGTH_REPARTI(self):
        """
        :description: Getter of the constant for the max length of the <utenti>reparti
        :return: self.__MAX_LENGTH_REPARTI, LITERAL[1000]
        """
        return self.__MAX_LENGTH_REPARTI
    
    @property
    def MAX_LENGTH_EMAIL(self):
        """
        :description: Getter of the constant for the max length of the <utenti>email
        :return: self.__MAX_LENGTH_EMAIL, LITERAL[255]
        """
        return self.__MAX_LENGTH_EMAIL
    
    @property
    def MAX_LENGTH_PASSWORD(self):
        """
        :description: Getter of the constant for the max length of the <utenti>password
        :return: self.__MAX_LENGTH_PASSWORD, LITERAL[255]
        """
        return self.__MAX_LENGTH_PASSWORD