from Classi.ClasseUtility.UtilityAutorizzazioni.ConstantsAutorizzazioni import ConstantsAutorizzazioni

class UtilityAutorizzazioni:
    """Class for the utility of autorizzazioni"""
      
    # Empty Constructor  
    def __init__(self) -> None:
        pass
    
    # Static methods
    @staticmethod
    def checkNome(nome:str) -> None:
        """
        :description: Static method to check if <autorizzazioni>nome is None the function will return None 
        and to check if <autorizzazioni>nome is more than constants.MAX_LENGTH_NOME the function will raise a ValueError
        :args: <autorizzazioni>nome:str
        :return: None | raise ValueError
        """
        if nome is None:
            return
        constants = ConstantsAutorizzazioni()
        if len(nome.strip()) > constants.MAX_LENGTH_NOME:
            raise ValueError(f"nome cannot be more than {constants.MAX_LENGTH_NOME} characters!")
        
    @staticmethod
    def checkFkListaFunzionalita(fkListaFunzionalita:str) -> None:
        """
        :description: Static method to check if <autorizzazioni>fkListaFunzionalita is None the function will return None 
        and to check if <autorizzazioni>fkListaFunzionalita is more than constants.MAX_LENGTH_NOME the function will raise a ValueError
        :args: <autorizzazioni>fkListaFunzionalita:str
        :return: None | raise ValueError
        """
        if fkListaFunzionalita is None:
            return
        constants = ConstantsAutorizzazioni()
        if len(fkListaFunzionalita.strip()) > constants.MAX_LENGTH_FK_LISTA_FUNZIONALITA:
            raise ValueError(f"fkListaFunzionalita cannot be more than {constants.MAX_LENGTH_FK_LISTA_FUNZIONALITA} characters!")