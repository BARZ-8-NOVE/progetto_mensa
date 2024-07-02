from Classi.ClasseMenu.Classe_t_menu.Repository_t_menu import RepositoryMenu
from datetime import datetime

class ServiceMenu:

    def __init__(self) -> None:
        self.repository = RepositoryMenu()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, data, fkTipoMenu, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.create(data, fkTipoMenu, dataInserimento, utenteInserimento)

    def update(self, id, data, fkTipoMenu, dataInserimento, utenteInserimento ):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.update(id, data, fkTipoMenu, dataInserimento, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
