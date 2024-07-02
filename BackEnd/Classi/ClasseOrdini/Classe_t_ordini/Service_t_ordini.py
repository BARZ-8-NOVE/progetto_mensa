from Classi.ClasseOrdini.Classe_t_ordini.Repository_t_ordini import RepositoryOrdini
from datetime import datetime

class ServiceOrdini:
    def __init__(self):
        self.repository = RepositoryOrdini()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, fkReparto, data, fkServizio, cognome, nome, letto, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()        
        return self.repository.create(fkReparto, data, fkServizio, cognome, nome, letto, dataInserimento, utenteInserimento)

    def update(self, id, fkReparto, data, fkServizio, cognome, nome, letto, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()        
        return self.repository.update(id, fkReparto, data, fkServizio, cognome, nome, letto, dataInserimento, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
