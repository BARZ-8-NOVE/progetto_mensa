from Classi.ClassePiatti.Classe_t_piatti.Repositroy_t_piatti import RepositoryPiatti
from datetime import datetime
class Service_t_Piatti:

    def __init__(self) -> None:
        self.repository = RepositoryPiatti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def get_by_fkTipoPiatto(self, fkTipoPiatto):
        return self.repository.get_by_fkTipoPiatto(fkTipoPiatto)
    
    #obsoleta non la usiamo piu sostituita 
    def get_tipipiatti_da_tipoPreparazione(self, id):
        id_modificato = None
        
        if id == 2:
            id_modificato = 1
        elif id == 3:
            id_modificato = 2
        elif id == 4:
            id_modificato = 3
        elif id == 5:
            id_modificato = 4
        elif id == 7:
            id_modificato = 5
        
        if id_modificato is not None:
            return self.repository.get_by_fkTipoPiatto(id_modificato)
        else:
            return None
    
    
    def create(self, fkTipoPiatto, codice, titolo, descrizione, inMenu, ordinatore, utenteInserimento, dataInserimento = None):
        return self.repository.create(fkTipoPiatto, codice, titolo, descrizione, inMenu, ordinatore, utenteInserimento, dataInserimento)


    def update(self, id, fkTipoPiatto, codice, titolo, descrizione, inMenu, ordinatore, utenteInserimento):
        return self.repository.update(id, fkTipoPiatto, codice, titolo, descrizione, inMenu, ordinatore, utenteInserimento)


    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
