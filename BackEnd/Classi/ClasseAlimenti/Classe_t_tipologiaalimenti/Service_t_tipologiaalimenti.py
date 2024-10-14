from .Repository_t_tipologiaalimenti import Repository_t_tipologiaalimenti

class Service_t_tipologiaalimenti:

    def __init__(self):
        self.repository = Repository_t_tipologiaalimenti()

    def get_all_tipologiaalimenti(self):
        return self.repository.get_all_tipologiaalimenti()

    def get_tipologiaalimenti_by_id(self, id):
        return self.repository.get_tipologiaalimenti_by_id(id)

    def create(self, nome, fktipologiaConservazione):
        return self.repository.create(nome, fktipologiaConservazione)
    
    def update(self, id, nome, fktipologiaConservazione):
        return self.repository.update(id, nome, fktipologiaConservazione)

    def delete(self, id):
        return self.repository.delete(id)
