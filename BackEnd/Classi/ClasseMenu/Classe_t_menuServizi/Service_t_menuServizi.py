from Classi.ClasseMenu.Classe_t_menuServizi.Repository_t_menuServizi import RepositoryMenuServizi
from datetime import datetime

class ServiceMenuServizi:

    def __init__(self) -> None:
        self.repository = RepositoryMenuServizi()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, fkMenu, fkServizio, note, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.create(fkMenu, fkServizio, note, dataInserimento, utenteInserimento)

    def update(self, id, fkMenu, fkServizio, note, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()        
        return self.repository.update(id, fkMenu, fkServizio, note, dataInserimento, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)

    def get_all_by_menu_ids(self, menu_ids):
        return self.repository.get_all_by_menu_ids(menu_ids)
    
    def get_all_by_menu_ids_con_servizio(self, menu_ids, fkServizio):
        return self.repository.get_all_by_menu_ids_con_servizio(menu_ids, fkServizio)