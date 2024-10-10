from Classi.ClasseSchede.Classe_t_schedePreconfezionate.Repository_t_schedePreconfezionate import RepositoryTSchedePreconfezionate
from datetime import datetime
class Service_t_SchedePreconfezionate:

    def __init__(self) -> None:
        self.repository = RepositoryTSchedePreconfezionate()

    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def get_all_by_fk_scheda(self, fkScheda):
        return self.repository.get_all_by_fk_scheda(fkScheda)
    
    def create(self, fkScheda, fkServizio, descrizione, note, ordinatore, utenteInserimento):
        return self.repository.create(fkScheda, fkServizio, descrizione, note, ordinatore, utenteInserimento)

    def update(self, id, fkServizio, descrizione, note, ordinatore, utenteInserimento):
        return self.repository.update(id, fkServizio, descrizione, note, ordinatore, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)

    
   