from Classi.ClasseUtility.UtilitiAlimenti.ConstantsAlimenti import ConstantsAlimenti

class UtilityAlimenti:

    def __init__(self) -> None:
        pass

    @staticmethod
    def check_nome_alimento(nome):
        if nome is None:
            raise TypeError('nome cannot be None!')
        nome = str(nome)
        if nome.strip() == "":
            raise ValueError('nome cannot be an empty string!')
        constantsAlimenti = ConstantsAlimenti()
        if len(nome.strip()) > constantsAlimenti.MAX_LENGTH_ALIMENTO:
            raise ValueError(f'alimento cannot be more than {constantsAlimenti.MAX_LENGTH_ALIMENTO} characters!')
        