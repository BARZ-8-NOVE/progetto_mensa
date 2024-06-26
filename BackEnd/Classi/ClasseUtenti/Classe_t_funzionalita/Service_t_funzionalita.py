from Classi.ClasseUtenti.Classe_t_funzionalita.Repository_t_funzionalita import Repository_t_funzionalita

class Service_t_funzionalita:

    def __init__(self) -> None:
        self.repository = Repository_t_funzionalita()

    def get_funzionalita_all(self):
        return self.repository.get_funzionalita_all()

    def get_funzionalita_by_id(self, id):
        return self.repository.get_funzionalita_by_id(id)
    
    def create_funzionalita(self, id, nome, frmNome):
        return self.repository.create_funzionalita(id, nome, frmNome)
    