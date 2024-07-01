from Classi.ClassePreparazioni.Classe_t_tipiquantita.Repository_t_tipiquantita import Repository_t_tipoquantita

class Service_t_tipoquantita:

    def __init__(self):
        self.repository = Repository_t_tipoquantita()

    def get_all_tipoquantita(self):
        return self.repository.get_all_tipoquantita()

    def get_tipoquantita_by_id(self, id):
        return self.repository.get_tipoquantita_by_id(id)

    def create_tipoquantita(self, tipo, peso_valore_in_grammi=None, peso_valore_in_Kg=None):
        return self.repository.create_tipoquantita(tipo, peso_valore_in_grammi, peso_valore_in_Kg)


    def update_tipoquantita(self, id, tipo, peso_valore_in_grammi=None, peso_valore_in_Kg=None):
        return self.repository.update_tipoquantita(id, tipo, peso_valore_in_grammi, peso_valore_in_Kg)

    def delete_tipoquantita(self, id):
        return self.repository.delete_tipoquantita(id)
