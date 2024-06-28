from Classi.ClasseMenu.Classe_t_tipiMenu.Repository_t_tipiMenu import RepositoryTipiMenu

class ServiceTipiMenu:
    def __init__(self) -> None:
        self.repository = RepositoryTipiMenu()

    def get_tipi_menu_all(self):
        return self.repository.get_tipi_menu_all()

    def get_tipi_menu_by_id(self, id):
        return self.repository.get_tipi_menu_by_id(id)

    def create_tipi_menu(self, descrizione, color, backgroundColor, ordinatore, dataInserimento, utenteInserimento):
        return self.repository.create_tipi_menu(descrizione, color, backgroundColor, ordinatore, dataInserimento, utenteInserimento)

    def delete_tipi_menu(self, id, dataCancellazione, utenteCancellazione):
        return self.repository.delete_tipi_menu(id, dataCancellazione, utenteCancellazione)
