from Classi.ClassePreparazioni.Classe_t_tipoPreparazioni.Repository_t_tipoPreparazioni import Repository_t_tipipreparazioni

class Service_t_tipipreparazioni:

    def __init__(self):
        self.repository = Repository_t_tipipreparazioni()

    def get_all_tipipreparazioni(self):
        return self.repository.get_all_tipipreparazioni()

    def get_tipipreparazioni_by_id(self, id):
        return self.repository.get_tipipreparazioni_by_id(id)

    def create_tipipreparazioni(self, descrizione):
        return self.repository.create_tipipreparazioni(descrizione)

    def update_tipipreparazioni(self, id, descrizione):
        return self.repository.update_tipipreparazioni(id, descrizione)

    def delete_tipipreparazioni(self, id):
        return self.repository.delete_tipipreparazioni(id)
