from Classi.ClasseAlimenti.Classe_t_allergeni.Repository_t_allergeni import RepositoryAllergeni

class Service_t_Allergeni:

    def __init__(self) -> None:
        self.repository = RepositoryAllergeni()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, nome):
        return self.repository.create(nome)

    def update(self, id, nome):
        return self.repository.update(id, nome)

    def delete(self, id):
        return self.repository.delete(id)
