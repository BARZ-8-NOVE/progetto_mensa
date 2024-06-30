from Classi.ClasseUtility.UtilityTipiUtenti.ConstantsTipiUtenti import ConstantsTipiUtenti

class UtilityTipiUtenti:

    def __init__(self) -> None:
        pass

    @staticmethod
    def checkFkAutorizzazioni(fkAutorizzazioni):
        if fkAutorizzazioni is None or isinstance(fkAutorizzazioni, int):
            return
        else:
            raise TypeError("fkAutorizzazioni can only be None or an integer!")

    @staticmethod
    def checkNomeTipoUtente(nomeTipoUtente:str):
        constants = ConstantsTipiUtenti()
        if len(nomeTipoUtente.strip()) > constants.MAX_LENGTH_NOME_TIPO_UTENTE:
            raise ValueError(f"nomeTipoUtente cannot be more than {constants.MAX_LENGTH_NOME_TIPO_UTENTE} characters!")