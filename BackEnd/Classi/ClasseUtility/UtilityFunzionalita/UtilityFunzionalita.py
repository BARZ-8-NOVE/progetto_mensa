from Classi.ClasseUtility.UtilityFunzionalita.ConstantsFunzionalita import ConstantsFunzionalita

class UtilityFunzionalita:

    def __init__(self) -> None:
        pass

    @staticmethod
    def checkNome(nome:str):
        constants = ConstantsFunzionalita()
        if len(nome.strip()) > constants.MAX_LENGTH_NOME:
            raise ValueError(f"nome cannot be more than {constants.MAX_LENGTH_NOME} characters!")
        
    @staticmethod
    def checkFrmNome(frmNome:str):
        constants = ConstantsFunzionalita()
        if len(frmNome.strip()) > constants.MAX_LENGTH_FRMNOME:
            raise ValueError(f"nome cannot be more than {constants.MAX_LENGTH_FRMNOME} characters!")