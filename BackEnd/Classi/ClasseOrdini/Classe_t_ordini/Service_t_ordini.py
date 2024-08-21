from Classi.ClasseOrdini.Classe_t_ordini.Repository_t_ordini import RepositoryOrdini
from datetime import datetime

class Service_t_Ordini:
    def __init__(self):
        self.repository = RepositoryOrdini()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, data, fkServizio):     
        return self.repository.create(data, fkServizio)
    
    def existing_Ordine(self, data, fkServizio):     
        return self.repository.existing_Ordine(data, fkServizio)


    def get_ordini_by_data(self, data, fkServizio):
        return self.repository.get_ordini_by_data(data, fkServizio)