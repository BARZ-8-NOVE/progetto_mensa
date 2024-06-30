class ConstantsFunzionalita:

    def __init__(self) -> None:
        pass
    
    __MAX_LENGTH_NOME = 50
    __MAX_LENGTH_FRMNOME = 50

    @property
    def MAX_LENGTH_NOME(self):
        return self.__MAX_LENGTH_NOME
    
    @property
    def MAX_LENGTH_FRMNOME(self):
        return self.__MAX_LENGTH_FRMNOME