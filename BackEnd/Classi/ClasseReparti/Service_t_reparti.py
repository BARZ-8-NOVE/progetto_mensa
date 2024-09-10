from Classi.ClasseReparti.Repository_t_reparti import RepositoryReparti
from datetime import datetime

class Service_t_Reparti:
    def __init__(self):
        self.repository = RepositoryReparti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    

    def get_by_ids(self, ids):
        return self.repository.get_by_ids(ids)

    def create(self, codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, utenteInserimento):
           
        return self.repository.create(codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, utenteInserimento)

    def update(self, id, codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, utenteInserimento):
       
        return self.repository.update(id, codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
