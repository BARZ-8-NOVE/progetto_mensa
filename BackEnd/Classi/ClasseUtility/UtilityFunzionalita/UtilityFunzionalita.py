from Classi.ClasseUtility.UtilityFunzionalita.ConstantsFunzionalita import ConstantsFunzionalita

class UtilityFunzionalita:
    """Class for the utility of funzionalita"""

    # Empty Constructor
    def __init__(self) -> None:
        pass

    # Static Methods
    @staticmethod
    def checkNome(nome:str):
        """
        :description: Static method to check if <funzionalita>nome is None the function will return None 
        and to check if <funzionalita>nome is more than constants.MAX_LENGTH_NOME the function will raise a ValueError
        :args: <funzionalita>nome:str
        :return: None | raise ValueError
        """
        if nome is None:
            return
        constants = ConstantsFunzionalita()
        if len(nome.strip()) > constants.MAX_LENGTH_NOME:
            raise ValueError(f"nome cannot be more than {constants.MAX_LENGTH_NOME} characters!")
        
    @staticmethod
    def checkFrmNome(frmNome:str):
        """
        :description: Static method to check if <funzionalita>frmNome is None the function will return None 
        and to check if <funzionalita>frmNome is more than constants.MAX_LENGTH_FRMNOME the function will raise a ValueError
        :args: <funzionalita>frmNome:str
        :return: None | raise ValueError
        """
        if frmNome is None:
            return
        constants = ConstantsFunzionalita()
        if len(frmNome.strip()) > constants.MAX_LENGTH_FRMNOME:
            raise ValueError(f"nome cannot be more than {constants.MAX_LENGTH_FRMNOME} characters!")