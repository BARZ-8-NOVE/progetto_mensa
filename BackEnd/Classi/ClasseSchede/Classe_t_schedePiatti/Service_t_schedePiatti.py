from Classi.ClasseSchede.Classe_t_schedePiatti.Repository_t_schedePiatti import RepositoryTSchedePiatti
from datetime import datetime
class Service_t_SchedePiatti:

    def __init__(self) -> None:
        self.repository = RepositoryTSchedePiatti()

    def  get_piatti_by_scheda(self, fkScheda):
        return  self.repository.get_piatti_by_scheda(fkScheda)
    
    def  get_piatti_by_scheda_and_servizio(self, fkScheda, fkServizio):
        return  self.repository.get_piatti_by_scheda_and_servizio(fkScheda, fkServizio)
    
    def create(self, fkScheda, fkServizio, fkPiatto, colonna, riga, note, ordinatore, dataInserimento):
        return  self.repository.get_piatti_by_scheda(fkScheda, fkServizio, fkPiatto, colonna, riga, note, ordinatore, dataInserimento)

    def delete_piatti_Scheda(self, fkScheda, utenteCancellazione):
        return  self.repository.delete_piatti_Scheda(fkScheda, utenteCancellazione)
    
    def get_piatti_non_dolci_by_scheda(self, fkScheda, fkServizio):
        return  self.repository.get_piatti_non_dolci_by_scheda(fkScheda, fkServizio)
    
    def get_dolci_pane_by_scheda(self, fkScheda, fkServizio):
        return  self.repository.get_dolci_pane_by_scheda(fkScheda, fkServizio)
