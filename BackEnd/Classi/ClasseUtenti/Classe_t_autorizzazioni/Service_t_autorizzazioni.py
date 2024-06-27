from Classi.ClasseUtenti.Classe_t_autorizzazioni.Repository_t_autorizzazioni import Repository_t_autorizzazioni

class Service_t_autorizzazioni:

    __MAX_LENGTH_NOME = 50
    __MAX_LENGTH_FKLISTAFUNZIONALITA = 1000

    def __init__(self) -> None:
        self.repository = Repository_t_autorizzazioni()

    def __checkNome(self, nome:str):
        if len(nome.strip()) > self.__MAX_LENGTH_NOME:
            raise ValueError(f"nome cannot be more than {self.__MAX_LENGTH_NOME} characters!")
        
    def __checkFkListaFunzionalita(self, fkListaFunzionalita:str):
        if len(fkListaFunzionalita.strip()) > self.__MAX_LENGTH_FKLISTAFUNZIONALITA:
            raise ValueError(f"nome cannot be more than {self.__MAX_LENGTH_FKLISTAFUNZIONALITA} characters!")
        
    def __checkId(self, id:int):
        if (id is None) or (id < 0) or (id == 0):
            raise ValueError("id cannot be None, 0, or less than 0!")
        
    def get_autorizzazioni_all(self):
        return self.repository.get_autorizzazioni_all()

    def get_autorizzazioni_by_id(self, id:int):
        return self.repository.get_autorizzazione_by_id(id)
    
    def create_autorizzazione(self, nome:str, fkListaFunzionalita:str):
        self.__checkNome(nome)
        self.__checkFkListaFunzionalita(fkListaFunzionalita)
        return self.repository.create_autorizzazione(nome, fkListaFunzionalita)
    
    def update_autorizzazione(self, id:int, nome:str, frmNome:str):
        self.__checkId(id)
        self.__checkNome(nome)
        self.__checkFkListaFunzionalita(frmNome)
        return self.repository.update_autorizzazione(id, nome, frmNome)
    
    def delete_autorizzazione(self, id:int):
        self.__checkId(id)
        return self.repository.delete_autorizzazione(id)