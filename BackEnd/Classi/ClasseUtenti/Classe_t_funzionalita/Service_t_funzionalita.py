from Classi.ClasseUtenti.Classe_t_funzionalita.Repository_t_funzionalita import Repository_t_funzionalita
from Classi.ClasseUtility.UtilityFunzionalita.UtilityFunzionalita import UtilityFunzionalita
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

class Service_t_funzionalita:

    def __init__(self) -> None:
        self.repository = Repository_t_funzionalita()

    def get_funzionalita_all(self):
        return self.repository.get_funzionalita_all()

    def get_funzionalita_by_id(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.get_funzionalita_by_id(id)
    
    def create_funzionalita(self, nome:str, frmNome:str):
        UtilityFunzionalita.checkNome(nome)
        UtilityFunzionalita.checkFrmNome(frmNome)
        return self.repository.create_funzionalita(nome, frmNome)
    
    def update_funzionalita_nome(self, id:int, nome:str):
        UtilityGeneral.checkId(id)
        UtilityFunzionalita.checkNome(nome)
        return self.repository.update_funzionalita_nome(id, nome)
    
    def update_funzionalita_frmNome(self, id:int, frmNome:str):
        UtilityGeneral.checkId(id)
        UtilityFunzionalita.checkFrmNome(frmNome)
        return self.repository.update_funzionalita_frmNome(id, frmNome)
    
    def delete_funzionalita(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.delete_funzionalita(id)
    