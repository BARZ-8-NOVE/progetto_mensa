class ConstantsAutorizzazioni:

    def __init__(self) -> None:
        pass

    __MAX_LENGTH_NOME = 50
    __MAX_LENGTH_FKLISTAFUNZIONALITA = 1000

    @property
    def MAX_LENGTH_NOME(self):
        return self.__MAX_LENGTH_NOME
    
    @property
    def MAX_LENGTH_FK_LISTA_FUNZIONALITA(self):
        return self.__MAX_LENGTH_FKLISTAFUNZIONALITA