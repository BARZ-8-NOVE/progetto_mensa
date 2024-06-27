from Classi.ClasseAlimenti.Classe_t_alimenti.Repository_t_alimenti import RepositoryAlimenti

class ServiceAlimenti:

    def __init__(self) -> None:
        self.repository = RepositoryAlimenti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, Alimento, Energia_Kcal, Energia_KJ, Prot_Tot_Gr, Glucidi_Tot, Lipidi_Tot, Saturi_Tot, fkAllergene, fkTipologiaAlimento):
        return self.repository.create(Alimento, Energia_Kcal, Energia_KJ, Prot_Tot_Gr, Glucidi_Tot, Lipidi_Tot, Saturi_Tot, fkAllergene, fkTipologiaAlimento)

    def update(self, id, Alimento, Energia_Kcal, Energia_KJ, Prot_Tot_Gr, Glucidi_Tot, Lipidi_Tot, Saturi_Tot, fkAllergene, fkTipologiaAlimento):
        return self.repository.update(id, Alimento, Energia_Kcal, Energia_KJ, Prot_Tot_Gr, Glucidi_Tot, Lipidi_Tot, Saturi_Tot, fkAllergene, fkTipologiaAlimento)

    def delete(self, id):
        return self.repository.delete(id)
