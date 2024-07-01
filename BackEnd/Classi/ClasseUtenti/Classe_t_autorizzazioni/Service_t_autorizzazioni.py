from Classi.ClasseUtenti.Classe_t_autorizzazioni.Repository_t_autorizzazioni import Repository_t_autorizzazioni
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityAutorizzazioni.UtilityAutorizzazioni import UtilityAutorizzazioni

class Service_t_autorizzazioni:

    def __init__(self) -> None:
        self.repository = Repository_t_autorizzazioni()
        
    def get_autorizzazioni_all(self):
        return self.repository.get_autorizzazioni_all()

    def get_autorizzazioni_by_id(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.get_autorizzazione_by_id(id)
    
    def create_autorizzazione(self, nome:str, fkListaFunzionalita:str):
        UtilityAutorizzazioni.checkNome(nome)
        UtilityAutorizzazioni.checkFkListaFunzionalita(fkListaFunzionalita)
        return self.repository.create_autorizzazione(nome, fkListaFunzionalita)
    
    def delete_autorizzazione(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.delete_autorizzazione(id)
    
    def update_autorizzazione_nome(self, id:int, nome:str):
        UtilityAutorizzazioni.checkNome(nome)
        UtilityGeneral.checkId(id)
        return self.repository.update_autorizzazione_nome(id, nome)
    
    def update_autorizzazione_fkListaFunzionalita(self, id:int, fkListaFunzionalita:str):
        UtilityAutorizzazioni.checkFkListaFunzionalita(fkListaFunzionalita)
        UtilityGeneral.checkId(id)
        return self.repository.update_autorizzazione_fkListaFunzionalita(id, fkListaFunzionalita)