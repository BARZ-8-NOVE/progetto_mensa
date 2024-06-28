from Classi.ClasseMenu.Classe_t_menu.Repository_t_menu import RepositoryMenu

class ServiceMenu:

    def __init__(self) -> None:
        self.repository = RepositoryMenu()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, data, fkTipoMenu, dataInserimento, utenteInserimento):
        return self.repository.create(data, fkTipoMenu, dataInserimento, utenteInserimento)

    def update(self, id, data, fkTipoMenu, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        return self.repository.update(id, data, fkTipoMenu, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
