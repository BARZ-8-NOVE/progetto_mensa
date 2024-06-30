class ConstantsUtenti:

    def __init__(self) -> None:
        pass
    
    __MAX_LENGTH_USERNAME = 50
    __MAX_LENGTH_NOME = 50
    __MAX_LENGTH_COGNOME = 50
    __MAX_LENGTH_FKFUNZCUSTOM = 1000
    __MAX_LENGTH_REPARTI = 1000
    __MAX_LENGTH_EMAIL = 255
    __MAX_LENGTH_PASSWORD = 255
    
    @property
    def MAX_LENGTH_USERNAME(self):
        return self.__MAX_LENGTH_USERNAME
    @property
    def MAX_LENGTH_NOME(self):
        return self.__MAX_LENGTH_NOME
    @property
    def MAX_LENGTH_COGNOME(self):
        return self.__MAX_LENGTH_COGNOME
    @property
    def MAX_LENGTH_FKFUNZCUSTOM(self):
        return self.__MAX_LENGTH_FKFUNZCUSTOM
    @property
    def MAX_LENGTH_REPARTI(self):
        return self.__MAX_LENGTH_REPARTI
    @property
    def MAX_LENGTH_EMAIL(self):
        return self.__MAX_LENGTH_EMAIL
    @property
    def MAX_LENGTH_PASSWORD(self):
        return self.__MAX_LENGTH_PASSWORD