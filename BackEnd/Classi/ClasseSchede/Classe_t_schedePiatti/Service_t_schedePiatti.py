from Classi.ClasseSchede.Classe_t_schedePiatti.Repository_t_schedePiatti import RepositoryTSchedePiatti
from datetime import datetime
class Service_t_SchedePiatti:

    def __init__(self) -> None:
        self.repository = RepositoryTSchedePiatti()


    def get_by_id(self, id):    
        return  self.repository.get_by_id(id)

    def  get_piatti_by_scheda(self, fkScheda):
        return  self.repository.get_piatti_by_scheda(fkScheda)
    
    def  get_piatti_by_scheda_and_servizio(self, fkScheda, fkServizio):
        return  self.repository.get_piatti_by_scheda_and_servizio(fkScheda, fkServizio)
    
    def create(self, fkScheda, fkServizio, fkPiatto, colonna, riga, note, ordinatore, utenteInserimento):
        return  self.repository.create(fkScheda, fkServizio, fkPiatto, colonna, riga, note, ordinatore, utenteInserimento)
    
    def update(self, id , fkScheda, fkServizio, fkPiatto, colonna, riga, note, ordinatore, utenteInserimento):
        return  self.repository.update(id, fkScheda, fkServizio, fkPiatto, colonna, riga, note, ordinatore, utenteInserimento)

    def delete_piatti_Scheda(self, fkScheda, utenteCancellazione):
        return  self.repository.delete_piatti_Scheda(fkScheda, utenteCancellazione)
    
    def get_piatti_non_dolci_by_scheda(self, fkScheda, fkServizio):
        return  self.repository.get_piatti_non_dolci_by_scheda(fkScheda, fkServizio)
    
    def get_dolci_pane_by_scheda(self, fkScheda, fkServizio):
        return  self.repository.get_dolci_pane_by_scheda(fkScheda, fkServizio)  

    def crea_piatto_vuoto(self, id):
        return  self.repository.crea_piatto_vuoto(id)

    def delete_piatto_singolo(self, id, utenteCancellazione):
        return  self.repository.delete_piatto_singolo(id, utenteCancellazione)