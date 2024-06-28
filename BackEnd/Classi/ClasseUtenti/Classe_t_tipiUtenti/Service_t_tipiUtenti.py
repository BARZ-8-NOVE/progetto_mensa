from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente

class Service_t_tipiUtenti:

    __MAX_LENGTH_NOMETIPOUTENTE = 50

    def __init__(self) -> None:
        self.repository = Repository_t_tipiUtente()

    def __checkFkAutorizzazioni(self, fkAutorizzazioni):
        if fkAutorizzazioni is None or isinstance(fkAutorizzazioni, int):
            return
        else:
            raise TypeError("fkAutorizzazioni can only be None or an integer!")

    def __checkNomeTipoUtente(self, nomeTipoUtente:str):
        if len(nomeTipoUtente.strip()) > self.__MAX_LENGTH_NOMETIPOUTENTE:
            raise ValueError(f"nomeTipoUtente cannot be more than {self.__MAX_LENGTH_NOMETIPOUTENTE} characters!")
        
    def __checkId(self, id:int):
        if (id is None) or (id < 0) or (id == 0):
            raise ValueError("id cannot be None, 0, or less than 0!")
        
    def get_tipiUtenti_all(self):
        return self.repository.get_tipiUtenti_all()

    def get_tipoUtente_by_id(self, id:int):
        self.__checkId(id)
        return self.repository.get_tipoUtente_by_id(id)
    
    def create_tipoUtente(self, nomeTipoUtente:str, fkAutorizzazioni):
        self.__checkFkAutorizzazioni(fkAutorizzazioni)
        self.__checkNomeTipoUtente(nomeTipoUtente)
        return self.repository.create_tipoUtente(nomeTipoUtente, fkAutorizzazioni)
    
    def update_tipoUtente(self, id:int, nomeTipoUtente:str, fkAutorizzazioni):
        self.__checkId(id)
        self.__checkNomeTipoUtente(nomeTipoUtente)
        self.__checkFkAutorizzazioni(fkAutorizzazioni)
        return self.repository.update_tipoUtente(id, nomeTipoUtente, fkAutorizzazioni)
    
    def delete_tipoUtente(self, id:int):
        self.__checkId(id)
        return self.repository.delete_tipoUtente(id)