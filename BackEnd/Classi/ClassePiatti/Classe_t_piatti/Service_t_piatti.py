from Classi.ClassePiatti.Classe_t_piatti.Repositroy_t_piatti import RepositoryPiatti

class ServicePiatti:

    def __init__(self) -> None:
        self.repository = RepositoryPiatti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        return self.repository.create(fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def update(self, id, fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        return self.repository.update(id, fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
