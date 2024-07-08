from Classi.ClasseAlimenti.Classe_t_alimenti.Repository_t_alimenti import RepositoryAlimenti
from Classi.ClasseUtility.UtilitiAlimenti.UtilityAlimenti import UtilityAlimenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

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
    
    def get_alimento_by_name(self, name):
        UtilityAlimenti.check_nome_alimento(name)
        name = str(name)
        return self.repository.get_alimento_by_name(name.upper())
    
    def get_alimenti_by_tipologia_alimento(self, tipologia_alimento):
        UtilityGeneral.safe_int_convertion(tipologia_alimento, 'tipologia alimento')
        return self.repository.get_alimenti_by_tipologia_alimento(tipologia_alimento)