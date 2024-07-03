from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Repository_t_ordiniPiatti import RepositoryOrdiniPiatti


class ServiceOrdiniPiatti:
    def __init__(self):
        self.repository = RepositoryOrdiniPiatti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, fkOrdineScheda, fkPiatto, quantita, note):       
        return self.repository.create(fkOrdineScheda, fkPiatto, quantita, note)

    def update(self, id, fkOrdineScheda, fkPiatto, quantita, note):       
        return self.repository.update(id, fkOrdineScheda, fkPiatto, quantita, note)

    def delete(self, id):
        return self.repository.delete(id)
