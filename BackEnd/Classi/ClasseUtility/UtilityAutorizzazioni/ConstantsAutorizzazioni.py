class ConstantsAutorizzazioni:
    """Class for the constants of autorizzazioni"""

    # Empty Constructor
    def __init__(self) -> None:
        pass

    # Constants
    __MAX_LENGTH_NOME = 50
    __MAX_LENGTH_FKLISTAFUNZIONALITA = 1000

    # Getters
    @property
    def MAX_LENGTH_NOME(self):
        """
        :description: Getter of the constant for the max length of the <autorizzazioni>nome
        :return: self.__MAX_LENGTH_NOME, LITERAL[50]
        """
        return self.__MAX_LENGTH_NOME
    
    @property
    def MAX_LENGTH_FK_LISTA_FUNZIONALITA(self):
        """
        :description: Getter of the constant for the max length of the <autorizzazioni>fkListaFunzionalita
        :return: self.__MAX_LENGTH_FKLISTAFUNZIONALITA, LITERAL[1000]
        """
        return self.__MAX_LENGTH_FKLISTAFUNZIONALITA