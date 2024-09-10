from Classi.ClasseMenu.Classe_t_tipiMenu.Repository_t_tipiMenu import RepositoryTipiMenu
from datetime import datetime

class Service_t_TipiMenu:
    def __init__(self) -> None:
        self.repository = RepositoryTipiMenu()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, descrizione, color, backgroundColor, ordinatore, utenteInserimento):

        return self.repository.create(descrizione, color, backgroundColor, ordinatore, utenteInserimento)

    def update(self, id, descrizione, color, backgroundColor, ordinatore, utenteInserimento):

        return self.repository.update(id, descrizione, color, backgroundColor, ordinatore, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
