class ConstantsFunzionalita:
    """Class for the constants of funzionalita"""
    
    # Empty Constructor
    def __init__(self) -> None:
        pass
    
    # Constants
    __MAX_LENGTH_NOME = 50
    __MAX_LENGTH_FRMNOME = 50

    # Getters
    @property
    def MAX_LENGTH_NOME(self):
        """
        :description: Getter of the constant for the max length of the <funzionalita>nome
        :return: self.__MAX_LENGTH_NOME, LITERAL[50]
        """
        return self.__MAX_LENGTH_NOME
    
    @property
    def MAX_LENGTH_FRMNOME(self):
        """
        :description: Getter of the constant for the max length of the <funzionalita>frmNome
        :return: self.__MAX_LENGTH_FRMNOME, LITERAL[50]
        """
        return self.__MAX_LENGTH_FRMNOME