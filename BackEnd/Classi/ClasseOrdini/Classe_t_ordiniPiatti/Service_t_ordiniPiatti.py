from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Repository_t_ordiniPiatti import RepositoryOrdiniPiatti


class Service_t_OrdiniPiatti:
    def __init__(self):
        self.repository = RepositoryOrdiniPiatti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def get_all_by_ordine_scheda(self, fkOrdineScheda):
         return self.repository.get_all_by_ordine_scheda(fkOrdineScheda)

    def create(self, fkOrdineScheda, fkPiatto, quantita, note):       
        return self.repository.create(fkOrdineScheda, fkPiatto, quantita, note)

    def update(self, id, fkOrdineScheda, fkPiatto, quantita, note):       
        return self.repository.update(id, fkOrdineScheda, fkPiatto, quantita, note)

    def delete(self, id):
        return self.repository.delete(id)
    
    def delete_by_fkOrdine(self, fkOrdineScheda):
        return self.repository.delete_by_fkOrdine(fkOrdineScheda)

    def get_count_piatti(self, data, servizio: int, fkReparto=None, fkScheda=None):
        return self.repository.get_count_piatti(data, servizio, fkReparto, fkScheda)