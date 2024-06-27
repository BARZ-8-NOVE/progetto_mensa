from Classi.ClasseUtenti.Classe_t_funzionalita.Repository_t_funzionalita import Repository_t_funzionalita

class Service_t_funzionalita:

    __MAX_LENGTH_NOME = 50
    __MAX_LENGTH_FRMNOME = 50

    def __init__(self) -> None:
        self.repository = Repository_t_funzionalita()

    def __checkNome(self, nome:str):
        if len(nome.strip()) > self.__MAX_LENGTH_NOME:
            raise ValueError(f"nome cannot be more than {self.__MAX_LENGTH_NOME} characters!")
        
    def __checkFrmNome(self, frmNome:str):
        if len(frmNome.strip()) > self.__MAX_LENGTH_FRMNOME:
            raise ValueError(f"nome cannot be more than {self.__MAX_LENGTH_FRMNOME} characters!")
        
    def __checkId(self, id:int):
        if (id is None) or (id < 0) or (id == 0):
            raise ValueError("id cannot be None, 0, or less than 0!")
        
    def get_funzionalita_all(self):
        return self.repository.get_funzionalita_all()

    def get_funzionalita_by_id(self, id:int):
        return self.repository.get_funzionalita_by_id(id)
    
    def create_funzionalita(self, nome:str, frmNome:str):
        self.__checkNome(nome)
        self.__checkFrmNome
        return self.repository.create_funzionalita(nome, frmNome)
    
    def update_funzionalita(self, id:int, nome:str, frmNome:str):
        self.__checkId(id)
        self.__checkNome(nome)
        self.__checkFrmNome(frmNome)
        return self.repository.update_funzionalita(id, nome, frmNome)
    
    def delete_funzionalita(self, id:int):
        self.__checkId(id)
        return self.repository.delete_funzionalita(id)
    