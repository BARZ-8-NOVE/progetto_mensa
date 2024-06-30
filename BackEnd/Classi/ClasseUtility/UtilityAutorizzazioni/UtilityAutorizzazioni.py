from Classi.ClasseUtility.UtilityAutorizzazioni.ConstantsAutorizzazioni import ConstantsAutorizzazioni

class UtilityAutorizzazioni:
      
    @staticmethod
    def checkNome(nome:str):
        constants = ConstantsAutorizzazioni()
        if len(nome.strip()) > constants.MAX_LENGTH_NOME:
            raise ValueError(f"nome cannot be more than {constants.MAX_LENGTH_NOME} characters!")
        
    @staticmethod
    def checkFkListaFunzionalita(fkListaFunzionalita:str):
        constants = ConstantsAutorizzazioni()
        if len(fkListaFunzionalita.strip()) > constants.MAX_LENGTH_FK_LISTA_FUNZIONALITA:
            raise ValueError(f"fkListaFunzionalita cannot be more than {constants.MAX_LENGTH_FK_LISTA_FUNZIONALITA} characters!")