from Classi.ClasseReparti.Repository_t_reparti import RepositoryReparti
from datetime import datetime

class Service_t_Reparti:
    def __init__(self):
        self.repository = RepositoryReparti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()        
        return self.repository.create(codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, dataInserimento, utenteInserimento)

    def update(self, id, codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()        
        return self.repository.update(id, codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, dataInserimento, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
