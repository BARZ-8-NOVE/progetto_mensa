from datetime import datetime
from Classi.ClassePiatti.Classe_t_tipiPiatti.Repositrory_t_tipiPiatti import RepositoryTipiPiatti

class ServiceTipiPiatti:

    def __init__(self) -> None:
        self.repository = RepositoryTipiPiatti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, descrizione, descrizionePlurale, inMenu, ordinatore, color, backgroundColor, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.create(descrizione, descrizionePlurale, inMenu, ordinatore, color, backgroundColor, dataInserimento, utenteInserimento)

    def update(self, id, descrizione, descrizionePlurale, inMenu, ordinatore, color, backgroundColor, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.update(id, descrizione, descrizionePlurale, inMenu, ordinatore, color, backgroundColor, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
