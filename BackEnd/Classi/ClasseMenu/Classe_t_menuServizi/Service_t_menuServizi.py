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
