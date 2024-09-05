from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente
from Classi.ClasseUtility.UtilityTipiUtenti.UtilityTipiUtenti import UtilityTipiUtenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

class Service_t_tipiUtenti:

    def __init__(self) -> None:
        self.repository = Repository_t_tipiUtente()
        
    def get_tipiUtenti_all(self):
        return self.repository.get_tipiUtenti_all()

    def get_tipoUtente_by_id(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.get_tipoUtente_by_id(id)
    
    def create_tipoUtente(self, nomeTipoUtente:str, fkAutorizzazioni):
        UtilityTipiUtenti.checkFkAutorizzazioni(fkAutorizzazioni)
        UtilityTipiUtenti.checkNomeTipoUtente(nomeTipoUtente)
        return self.repository.create_tipoUtente(nomeTipoUtente, fkAutorizzazioni)
    
    def update_tipoUtente_nomeTipoUtente(self, id:int, nomeTipoUtente:str):
        UtilityGeneral.checkId(id)
        UtilityTipiUtenti.checkNomeTipoUtente(nomeTipoUtente)
        return self.repository.update_tipoUtente_nomeTipoUtente(id, nomeTipoUtente)
    
    def update_tipoUtente_fkAutorizzazioni(self, id:int, fkAutorizzazioni):
        UtilityGeneral.checkId(id)
        UtilityTipiUtenti.checkFkAutorizzazioni(fkAutorizzazioni)
        return self.repository.update_tipoUtente_fkAutorizzazioni(id, fkAutorizzazioni)
    
    def delete_tipoUtente(self, id:int):
        UtilityGeneral.checkId(id)
        return self.repository.delete_tipoUtente(id)
    
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, nomeTipoUtente, fkAutorizzazioni = None):
        return self.repository.create(nomeTipoUtente, fkAutorizzazioni)
    
    def update(self, id, nomeTipoUtente, fkAutorizzazioni = None):
        return self.repository.update(id, nomeTipoUtente, fkAutorizzazioni)