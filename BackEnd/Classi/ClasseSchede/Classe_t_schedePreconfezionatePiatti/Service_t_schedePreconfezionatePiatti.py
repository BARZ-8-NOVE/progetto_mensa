from Classi.ClasseSchede.Classe_t_schedePreconfezionatePiatti.Repository_t_schedePreconfezionatePiatti import RepositoryTSchedePreconfezionatePiatti
from datetime import datetime
class Service_t_SchedePreconfezionatePiatti:

    def __init__(self) -> None:
        self.repository = RepositoryTSchedePreconfezionatePiatti()


    def get_by_id(self, id):    
        return  self.repository.get_by_id(id)

    def  get_piatti_by_scheda(self, fkScheda):
        return  self.repository.get_piatti_by_scheda(fkScheda)
    
    def create(self, fkSchedaPreconfezionata, fkPiatto, quantita, utenteInserimento):
        return  self.repository.create(fkSchedaPreconfezionata, fkPiatto, quantita, utenteInserimento)

    def update(self, id, fkSchedaPreconfezionata, fkPiatto, quantita, utenteInserimento):
        return  self.repository.update(id, fkSchedaPreconfezionata, fkPiatto, quantita, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return  self.repository.delete(id, utenteCancellazione)
    
    def delete_by_fkSchedaPreconfezionata(self, fkSchedaPreconfezionata, utenteCancellazione):
        return  self.repository.delete_by_fkSchedaPreconfezionata(fkSchedaPreconfezionata, utenteCancellazione)