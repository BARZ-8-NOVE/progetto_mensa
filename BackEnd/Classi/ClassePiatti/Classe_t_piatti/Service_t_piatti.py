from Classi.ClassePiatti.Classe_t_piatti.Repositroy_t_piatti import RepositoryPiatti
from datetime import datetime
class ServicePiatti:

    def __init__(self) -> None:
        self.repository = RepositoryPiatti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.create(fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento)

    def update(self, id, fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.update(id, fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
