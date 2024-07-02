class ConstantsTipiUtenti:
    """Class for the constants of tipiUtenti"""

    # Empty Constructor
    def __init__(self) -> None:
        pass
    
    # Constant
    __MAX_LENGTH_NOME_TIPO_UTENTE = 50

    # Getter
    @property
    def MAX_LENGTH_NOME_TIPO_UTENTE(self):
        """
        :description: Getter of the constant for the max length of the <tipiUtenti>nomeTipoUtente
        :return: self.__MAX_LENGTH_NOME_TIPO_UTENTE, LITERAL[50]
        """
        return self.__MAX_LENGTH_NOME_TIPO_UTENTE