from Classi.ClasseAlimenti.Classe_t_tipologiaalimenti.Repository_t_tipologiaalimenti import RepositoryTipologiaAlimenti

class ServiceTipologiaAlimenti:

    def __init__(self) -> None:
        self.repository = RepositoryTipologiaAlimenti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, nome, descrizione, conservazione_id):
        return self.repository.create(nome, descrizione, conservazione_id)

    def update(self, id, nome, descrizione, conservazione_id):
        return self.repository.update(id, nome, descrizione, conservazione_id)

    def delete(self, id):
        return self.repository.delete(id)
