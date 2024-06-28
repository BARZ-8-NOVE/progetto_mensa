from Classi.ClasseServizi.Repository_t_servizi import RepositoryTServizi

class ServiceTServizi:
    def __init__(self) -> None:
        self.repository = RepositoryTServizi()

    def get_all_servizi(self):
        return self.repository.get_all_servizi()

    def get_servizio_by_id(self, id):
        return self.repository.get_servizio_by_id(id)

    def create_servizio(self, descrizione, ordinatore, inMenu):
        return self.repository.create_servizio(descrizione, ordinatore, inMenu)

    def update_servizio(self, id, descrizione=None, ordinatore=None, inMenu=None):
        return self.repository.update_servizio(id, descrizione, ordinatore, inMenu)

    def delete_servizio(self, id):
        return self.repository.delete_servizio(id)
