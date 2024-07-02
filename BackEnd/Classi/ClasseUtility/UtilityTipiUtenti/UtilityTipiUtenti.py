from Classi.ClasseUtility.UtilityTipiUtenti.ConstantsTipiUtenti import ConstantsTipiUtenti

class UtilityTipiUtenti:
    """Class for the utility of tipiUtenti"""

    # Empty Constructor
    def __init__(self) -> None:
        pass

    # Static methods
    @staticmethod
    def checkFkAutorizzazioni(fkAutorizzazioni):
        """
        :description: Static method to check if <tipiutenti>fkAutorizzazioni is None 
        or isinstance of an integer the function will return None 
        else the function will raise a TypeError
        :args: <tipiutenti>fkAutorizzazioni
        :return: None | raise TypeError
        """
        if fkAutorizzazioni is None or isinstance(fkAutorizzazioni, int):
            return
        else:
            raise TypeError("fkAutorizzazioni can only be None or an integer!")

    @staticmethod
    def checkNomeTipoUtente(nomeTipoUtente:str):
        """
        :description: Static method to check if <tipiUtenti>nomeTipoUtente is None the function will return None 
        and to check if <tipiUtenti>nomeTipoUtente is more than constants.MAX_LENGTH_NOME_TIPO_UTENTE the function will raise a ValueError
        :args: <tipiUtenti>nomeTipoUtente:str
        :return: None | raise ValueError
        """
        if nomeTipoUtente is None:
            return
        constants = ConstantsTipiUtenti()
        if len(nomeTipoUtente.strip()) > constants.MAX_LENGTH_NOME_TIPO_UTENTE:
            raise ValueError(f"nomeTipoUtente cannot be more than {constants.MAX_LENGTH_NOME_TIPO_UTENTE} characters!")